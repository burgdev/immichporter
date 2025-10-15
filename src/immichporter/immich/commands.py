"""Immich CLI commands."""

import time
import click
import sys
from rich.progress import Progress, SpinnerColumn, BarColumn
import functools
from loguru import logger
from immichporter.commands import logging_options
from rich.console import Console
from rich.table import Table
from rich.progress import (
    TextColumn,
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
from immichporter.immich.db import ImmichDBClient
from immichporter.database import get_db_session as get_sqlite_session
from immichporter.models import User
from immichporter.immich.client.models import (
    JobName,
)


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
    """Update our photos with their Immich IDs by searching for them in Immich."""
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
    """Sync albums from our database to Immich."""
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
    """Update our users with their Immich IDs by searching for them in Immich."""
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


@cli_immich.command("adjust-owners")
@immich_options
@click.option(
    "--db-host",
    envvar="DB_HOST",
    default="database",
    help="PostgreSQL host. Can also be set via DB_HOST environment variable.",
    show_envvar=True,
    show_default=True,
)
@click.option(
    "--db-port",
    envvar="DB_PORT",
    default=5432,
    type=int,
    help="PostgreSQL port. Can also be set via DB_PORT environment variable.",
    show_envvar=True,
    show_default=True,
)
@click.option(
    "--db-username",
    envvar="DB_USERNAME",
    default="immich",
    help="PostgreSQL username. Can also be set via DB_USERNAME environment variable.",
    show_envvar=True,
    show_default=True,
)
@click.option(
    "--db-password",
    envvar="DB_PASSWORD",
    default="immich",
    help="PostgreSQL password. Can also be set via DB_PASSWORD environment variable.",
    show_envvar=True,
    show_default=False,
    hide_input=True,
)
@click.option(
    "--db-name",
    envvar="DB_NAME",
    default="immich",
    help="PostgreSQL database name. Can also be set via DB_NAME environment variable.",
    show_envvar=True,
    show_default=True,
)
@click.option(
    "--dry-run/--no-dry-run",
    is_flag=True,
    default=True,
    help="Show what would be changed without making any changes",
    show_default=True,
)
@click.option(
    "--batch-size",
    default=25,
    type=int,
    help="Number of assets to process in a batch",
    show_default=True,
)
@click.option(
    "--storage-migration/--no-storage-migration",
    is_flag=True,
    default=True,
    help="Run 'storage template migration' job after adjusting owners",
    show_default=True,
)
@click.option(
    "--db-backup/--no-db-backup",
    is_flag=True,
    default=True,
    help="Run 'storage template migration' job after adjusting owners",
    show_default=True,
)
@logging_options
def adjust_owners_command(
    immich: ImmichClient,
    db_host: str,
    db_port: int,
    db_username: str,
    db_password: str,
    db_name: str,
    dry_run: bool,
    batch_size: int,
    log_level: str,
    storage_migration: bool,
    db_backup: bool,
    **options,
):
    """Adjust asset ownership in Immich based on SQLite database."""
    log_level = options.get("log_level", "INFO").upper()

    if db_backup:
        console.print("[yellow]Running database backup...[/]")
        console.print("[dim]wait 2 minutes...[/]")
        immich.run_db_backup(180)

    # Construct PostgreSQL URL
    postgres_url = (
        f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    if log_level == "DEBUG":
        console.print(
            f"[yellow]Using PostgreSQL URL: {postgres_url.split('@')[0]}@...[/]"
        )

    try:
        # Initialize Immich DB client
        immich_client = ImmichDBClient(postgres_url, echo=(log_level == "DEBUG"))
    except Exception as e:
        console.print(f"[red]Error connecting to Immich database: {e}[/]")
        return

    try:
        # Get SQLite session
        db_session = get_sqlite_session()

        # Get all users with add_to_immich=True
        users = db_session.query(User).filter(User.add_to_immich == True).all()  # noqa: E712
        if not users:
            console.print("[yellow]No users found with add_to_immich=True[/]")
            return

        console.print(f"Found {len(users)} users to process")

        for user in users:
            if not user.immich_user_id:
                console.print(
                    f"[yellow]Skipping user {user.source_name}: No immich_user_id[/]"
                )
                continue

            # Get all photos for this user
            photos = db_session.query(Photo).filter(Photo.user_id == user.id).all()
            if not photos:
                console.print(f"[yellow]No photos found for user {user.source_name}[/]")
                continue

            # Extract immich_ids from photos
            immich_ids = [str(photo.immich_id) for photo in photos if photo.immich_id]

            if not immich_ids:
                console.print(
                    f"[yellow]No valid immich_ids found for user {user.source_name}[/]"
                )
                continue

            console.print(
                f"\nProcessing user [blue]#{user.id}[/]: [yellow]{user.source_name} <{user.immich_email}>[/][dim with {len(immich_ids)} assets]"
            )
            console.print(f"Immich User ID: {user.immich_user_id}")

            if dry_run:
                console.print(
                    "[yellow]Dry run: Would update asset ownership in batches[/]"
                )
                continue

            # Count how many assets actually need updating
            total_to_update = immich_client.count_assets_needing_owner_update(
                asset_ids=immich_ids, new_owner_id=str(user.immich_user_id)
            )

            if total_to_update == 0:
                console.print("[green]✓ All assets already have the correct owner[/]")
                continue

            console.print(
                f"[yellow]Found [blue]{total_to_update}[/] assets to update...[/]"
            )

            with Progress(
                SpinnerColumn(),
                "[progress.description]{task.description}",
                BarColumn(bar_width=30),
                "[progress.percentage]{task.percentage:>3.0f}%",
                "•",
                "[cyan]{task.completed}/{task.total} assets",
                console=console,
            ) as progress:
                task = progress.add_task(
                    f"[cyan]Updating assets for user {user.immich_user_id}[/]",
                    total=total_to_update,
                )

                # Process batches
                for i in range(0, len(immich_ids), batch_size):
                    batch = immich_ids[i : i + batch_size]
                    try:
                        updated = immich_client.update_asset_owner(
                            asset_ids=batch, new_owner_id=str(user.immich_user_id)
                        )
                        if (
                            updated > 0
                        ):  # Only update progress if something was actually updated
                            progress.update(
                                task,
                                advance=updated,
                                description=f"[cyan]Updating assets for user {user.immich_user_id}[/]",
                            )
                            time.sleep(0.1)  # Small delay to allow progress to update
                    except Exception as e:
                        progress.console.print(
                            f"[red]Error updating batch {i // batch_size + 1}: {e}[/]"
                        )
                        continue

    except Exception as e:
        console.print(f"[red]Error during database operations: {e}[/]")
        return
    finally:
        if "db_session" in locals():
            db_session.close()

    if storage_migration:
        console.print(
            "\nStarting 'storage template migration' job, this can take some time ..."
        )
        started = immich.start_job(JobName.STORAGETEMPLATEMIGRATION)
        if not started:
            console.print(
                "[red]Failed to start 'storage template migration' job, please start it manually[/]"
            )
            sys.exit(1)

        with Progress(
            SpinnerColumn(),
            "[progress.description]{task.description}",
            "•",
            "[elapsed]Elapsed: {task.fields[elapsed_time]}",
            console=console,
        ) as progress:
            start_time = time.time()
            task = progress.add_task(
                "[cyan]Running storage template migration...", elapsed_time="0:00:00"
            )

            job_status = immich.get_job_status(JobName.STORAGETEMPLATEMIGRATION)
            while job_status.job_counts.active > 0:
                elapsed = time.time() - start_time
                elapsed_str = time.strftime("%H:%M:%S", time.gmtime(elapsed))
                progress.update(
                    task,
                    description="[cyan]Running storage template migration...",
                    elapsed_time=elapsed_str,
                    refresh=True,
                )
                time.sleep(1)
                job_status = immich.get_job_status(JobName.STORAGETEMPLATEMIGRATION)

            progress.update(
                task,
                description="[green]Storage template migration complete!",
                elapsed_time=time.strftime(
                    "%H:%M:%S", time.gmtime(time.time() - start_time)
                ),
                refresh=True,
            )
