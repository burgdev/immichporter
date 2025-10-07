"""Immich CLI commands."""

import click
import sys
import functools
from loguru import logger
from immichporter.commands import logging_options
from rich.console import Console
from rich.table import Table
import time
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TimeRemainingColumn,
    TimeElapsedColumn,
)

from immichporter.utils import generate_password
from datetime import datetime
from immichporter.immich.immich import ImmichClient, immich_api_client
from immichporter.database import (
    get_db_session,
    get_photos_from_db,
    get_albums_without_immich_id,
    get_users,
)
from immichporter.immich.client.models import AlbumUserCreateDto, AlbumUserRole
from immichporter.immich.client.api.users import get_my_user
from immichporter.models import Photo


def format_time(seconds: float) -> str:
    """Format time in seconds to a human-readable string (e.g., '1h 23m 45s' or '5m 23s')."""
    if seconds is None or seconds < 0:
        return "Calculating..."
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"{hours}h {minutes:02d}m {seconds:02d}s"
    return f"{minutes:02d}m {seconds:02d}s"


console = Console()

# Create a Click command group
cli_immich = click.Group("immich", help="Immich commands")


def immich_options(f):
    """Common options for Immich commands."""

    @click.option(
        "--endpoint",
        envvar="IMMICH_ENDPOINT",
        default="http://localhost:2283",
        help="Immich server URL (default: http://localhost:2283)",
        show_default=True,
        show_envvar=True,
    )
    @click.option(
        "-k",
        "--api-key",
        envvar="IMMICH_API_KEY",
        required=True,
        help="Immich API key",
        show_envvar=True,
    )
    @click.option(
        "--insecure",
        is_flag=True,
        envvar="IMMICH_INSECURE",
        help="Skip SSL certificate verification",
        show_envvar=True,
    )
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        endpoint = kwargs["endpoint"]
        api_key = kwargs["api_key"]
        insecure = kwargs["insecure"]
        client_api = immich_api_client(
            endpoint=endpoint, api_key=api_key, insecure=insecure
        )
        kwargs["immich_api"] = client_api
        kwargs["immich"] = ImmichClient(client=client_api)
        return f(*args, **kwargs)

    return wrapper


# Add commands to the immich group
@cli_immich.command()
@immich_options
@click.option(
    "--limit", type=int, default=50, help="Maximum number of albums to return"
)
@click.option("--shared/--no-shared", default=None, help="Filter by shared status")
@logging_options
def list_albums(immich: ImmichClient, limit, shared, **options):
    """List all albums on the Immich server."""
    logger.info(f"Fetching albums from '{immich.endpoint}'")

    try:
        albums = immich.get_albums(limit=limit, shared=shared)
        logger.info(f"Retrieved {len(albums) if albums else 0} albums")

        if not albums:
            console.print("[red]No albums found.[/]")
            return

        # Create a table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=36)
        table.add_column("Album Name")
        table.add_column("Asset Count")
        table.add_column("Shared")
        table.add_column("Created At")

        for album in albums:
            table.add_row(
                str(album.id),
                album.album_name,
                str(album.asset_count),
                "✓" if album.shared else "✗",
                album.created_at.strftime("%Y-%m-%d %H:%M")
                if hasattr(album, "created_at")
                else "N/A",
            )

        # Render the table
        console.print(table)
    except Exception as e:
        logger.error(f"Error fetching albums: {str(e)}")


@cli_immich.command()
@immich_options
@click.option(
    "--dry-run",
    is_flag=True,
    help="Run without making any changes",
    default=False,
)
@logging_options
def update_photos(immich: ImmichClient, dry_run: bool, **options):
    """Update photos with their Immich IDs by searching for them in Immich."""
    logger.info("Starting photo update process")

    # Get photos without immich_id
    session = get_db_session()
    photos = get_photos_from_db(session, has_immich_id=False)

    if not photos:
        logger.info("All photos already have immich_ids")
        return

    if dry_run:
        console.print("[yellow]\n DRY RUN MODE - No changes will be made\n[/yellow]")
        console.print("[yellow]\n🚧 DRY RUN MODE - No changes will be made\n[/yellow]")

    logger.info(f"Found {len(photos)} photos without immich_id")

    from concurrent.futures import ThreadPoolExecutor, as_completed

    # Initialize counters
    updated_count = 0
    not_found_count = 0

    # Configure progress bar with total count and improved time display
    progress_columns = [
        TextColumn("Updating photos", style="white"),
        BarColumn(
            bar_width=None,  # Will use full width
            complete_style="blue",
            finished_style="green",
            pulse_style="white",
        ),
        TextColumn("[white]{task.percentage:>3.0f}%[/white]", justify="right"),
        TextColumn("•", style="white"),
        TextColumn("[white]{task.completed}[/]/[blue]{task.total}[/]", justify="right"),
        TextColumn("[red]({task.fields[not_found]} not found)[/red]", justify="left"),
        TextColumn("•", style="white"),
        TimeElapsedColumn(),
        TextColumn("(ETA:", style="white"),
        TimeRemainingColumn(compact=True),
        TextColumn(")", style="white"),
    ]

    def process_photo(photo_id, filename, date_taken, immich, dry_run):
        """Process a single photo and return the result.

        Args:
            photo_id: The ID of the photo in the database
            filename: The filename of the photo
            date_taken: The date the photo was taken (optional)
            immich: The Immich client instance
            dry_run: Whether this is a dry run

        Returns:
            tuple: (photo_id, matched_asset_id, error_message)
        """
        try:
            # First try with both filename and date
            results = immich.search_assets(filename=filename, taken=date_taken)

            # If no results, try with just the filename
            if not results:
                results = immich.search_assets(filename=filename)

            if results:
                return photo_id, results[0].id, None  # Return first match ID
            else:
                return photo_id, None, "not_found"

        except Exception as e:
            return photo_id, None, str(e)

    with Progress(
        *progress_columns,
        console=console,
        transient=True,
        refresh_per_second=10,
        speed_estimate_period=30.0,
    ) as progress:
        # Initialize task with proper time formatting
        task = progress.add_task(
            "[cyan]Updating photos...", total=len(photos), completed=0, not_found=0
        )

        # Process photos in batches
        BATCH_SIZE = 20
        MAX_WORKERS = 5

        for i in range(0, len(photos), BATCH_SIZE):
            batch = photos[i : i + BATCH_SIZE]
            batch_updates = []

            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                # Submit all photos in the current batch with just the data we need
                future_to_photo_id = {
                    executor.submit(
                        process_photo,
                        photo.id,
                        photo.filename,
                        photo.date_taken if hasattr(photo, "date_taken") else None,
                        immich,
                        dry_run,
                    ): photo.id
                    for photo in batch
                }

                # Process completed futures as they complete
                for future in as_completed(future_to_photo_id):
                    photo_id, matched_asset_id, error = future.result()

                    # Get the photo object from the database to ensure it's fresh
                    try:
                        photo = session.get(Photo, photo_id)
                        if not photo:
                            logger.warning(
                                f"Photo with ID {photo_id} not found in database"
                            )
                            not_found_count += 1
                            continue

                        if error == "not_found":
                            logger.info(f"No match found for {photo.filename}")
                            not_found_count += 1
                        elif error:
                            logger.error(f"Error processing {photo.filename}: {error}")
                            continue
                        else:
                            # Add to batch updates
                            batch_updates.append(
                                {
                                    "id": photo.id,
                                    "immich_id": matched_asset_id,
                                    "updated_at": datetime.utcnow(),
                                }
                            )
                            updated_count += 1

                    except Exception as e:
                        logger.error(f"Error updating photo {photo_id}: {str(e)}")
                        continue

                    # Update progress
                    progress.update(
                        task,
                        advance=1,
                        completed=min(updated_count + not_found_count, len(photos)),
                        not_found=not_found_count,
                    )

            # Process batch updates
            if batch_updates:
                if not dry_run:
                    try:
                        # Update all photos in the batch at once
                        session.bulk_update_mappings(Photo, batch_updates)
                        session.commit()
                        logger.debug(f"Updated {len(batch_updates)} photos in batch")
                    except Exception as e:
                        session.rollback()
                        logger.error(f"Error updating batch: {str(e)}")
                else:
                    logger.debug(
                        f"[DRY RUN] Would update {len(batch_updates)} photos in batch"
                    )

            # Small delay between batches to avoid overwhelming the server
            time.sleep(0.1)

    # Log summary
    logger.info(f"Update complete. Processed {len(photos)} photos:")
    logger.info(f"  • Successfully updated: {updated_count}")
    logger.info(f"  • Not found: {not_found_count}")

    if not dry_run:
        logger.success(f"Successfully updated {updated_count} photos in Immich")
    else:
        logger.info(f"Dry run complete. Would update {updated_count} photos")


@cli_immich.command()
@immich_options
@click.option("-a", "--all", is_flag=True, help="Delete all albums")
@click.option(
    "-n",
    "--dry-run",
    is_flag=True,
    help="Run without making any changes",
    default=False,
)
@logging_options
def delete_albums(immich: ImmichClient, all: bool, dry_run: bool, **options):
    """Delete albums from Immich."""
    logger.info("Starting album deletion process")
    albums = immich.get_albums()
    if all:
        for album in albums:
            if not dry_run:
                immich.delete_album(album.id)
            else:
                console.print(
                    f"[yellow]DRY RUN:[/] Would delete album: [blue]{album.album_name}[/]"
                )


@cli_immich.command()
@immich_options
@click.option(
    "--limit", type=int, default=None, help="Limit the number of albums to sync"
)
@click.option(
    "-n",
    "--dry-run",
    is_flag=True,
    help="Run without making any changes",
    default=False,
)
@logging_options
def sync_albums(immich: ImmichClient, limit: int | None, dry_run: bool, **options):
    """Sync albums from database to Immich."""
    logger.info("Starting album sync process")

    session = get_db_session()

    # Get albums that haven't been synced to Immich yet
    albums = get_albums_without_immich_id(session)
    if limit:
        albums = albums[:limit]

    if not albums:
        logger.info("All albums already synced to Immich")
        return

    if dry_run:
        console.print("[yellow]\n🚧 DRY RUN MODE - No changes will be made\n[/yellow]")

    logger.info(f"Found {len(albums)} albums to sync")

    # Configure progress bar
    progress_columns = [
        TextColumn("Syncing albums", style="white"),
        BarColumn(bar_width=None, complete_style="blue", finished_style="green"),
        TextColumn("[white]{task.percentage:>3.0f}%[/white]", justify="right"),
        TextColumn("•", style="white"),
        TextColumn("[white]{task.completed}/{task.total}", justify="right"),
    ]

    my_user = get_my_user.sync(client=immich.client)
    if my_user is None:
        logger.error("Failed to get my user")
        sys.exit(1)

    with Progress(*progress_columns, console=console) as progress:
        task = progress.add_task("Syncing albums...", total=len(albums))

        for album in albums:
            try:
                # Get album users with immich_id
                album_users = [
                    AlbumUserCreateDto(
                        user_id=user.immich_user_id, role=AlbumUserRole.VIEWER
                    )
                    for user in album.users
                    if user.immich_user_id is not None
                    and user.immich_user_id != my_user.id
                ]
                album_user_names = [
                    user.immich_name for user in album.users if user.immich_name
                ]

                # Get album photos with immich_id
                photos = get_photos_from_db(
                    session, album_id=album.id, has_immich_id=True
                )
                photo_ids = [photo.immich_id for photo in photos]
                album_name = (
                    album.immich_title if album.immich_title else album.source_title
                )

                if dry_run:
                    progress.console.print("[yellow][DRY RUN][/]")
                progress.console.print(
                    f"Create album: [blue]{album_name}[/] with [blue]{len(photo_ids)}[/] photos"
                )
                if album_user_names:
                    progress.console.print(f"[dim]{', '.join(album_user_names)}[/]")
                if not dry_run:
                    # Create album in Immich
                    immich_album = immich.create_album(
                        name=album_name,
                        description=None,
                        users=album_users,
                        assets=photo_ids,
                    )

                    # Update album with immich_id
                    album.immich_id = immich_album.id
                    session.add(album)
                    session.commit()
                else:
                    time.sleep(0.1)

            except Exception as e:
                logger.error(f"Error syncing album {album.source_title}: {str(e)}")
                session.rollback()
            finally:
                progress.update(task, advance=1)

    logger.info("Album sync complete")


@cli_immich.command()
@immich_options
@click.option(
    "--dry-run",
    is_flag=True,
    help="Run without making any changes",
    default=False,
)
@logging_options
def update_users(immich: ImmichClient, dry_run: bool, **options):
    """Update photos with their Immich IDs by searching for them in Immich."""
    logger.info("Starting users update process")
    session = get_db_session()
    db_users = get_users(session)
    immich_users = immich.get_users()
    for db_user in db_users:
        if not db_user.add_to_immich:
            continue
        immich_name = db_user.immich_name
        immich_email = db_user.immich_email
        mail_fmt = f"{immich_email}"
        console.print(f"{immich_name:<20} [blue]{mail_fmt:<30}[/]", end="")
        set_immich_id = db_user.immich_user_id
        immich_id = set_immich_id
        if not immich_id:  # check for email
            for immich_user in immich_users:
                if immich_user.email == immich_email:
                    immich_id = immich_user.id
                    break
        if not immich_id:  # check for name
            for immich_user in immich_users:
                if immich_user.name == immich_name:
                    immich_id = immich_user.id
                    break
        if set_immich_id is None and immich_id:  # add to DB
            if not dry_run:
                console.print(f"add id: {immich_id}")
                db_user.immich_user_id = immich_id
                session.add(db_user)
                session.commit()
            else:
                console.print(f"[yellow][DRY RUN][/] add id: {immich_id}")
        elif set_immich_id is not None:
            console.print(f"[green]id already set: {immich_id}[/]")
        else:
            # create new user
            password = generate_password()
            if not dry_run:
                immich.add_user(
                    name=immich_name, email=immich_email, password=password, quota_gb=15
                )
                console.print("[red]add user to immich")
                db_user.immich_initial_password = password
                session.add(db_user)
                session.commit()
            else:
                console.print("[yellow][DRY RUN][/] add user to immich")
        # console.print(f"{immich_name} <[blue]{immich_email}[/]> ({immich_id if immich_id else '[red]not set[/]'})")
