"""Google Photos CLI commands."""

import asyncio
import click
from rich.console import Console

from loguru import logger

from immichporter.database import get_db_session, get_database_stats, init_database
from immichporter.gphotos.scraper import GooglePhotosScraper
from immichporter.gphotos.settings import playwright_session_dir
from immichporter.commands import logging_options, database_options

# Create a Click command group
cli_gphotos = click.Group("gphotos", help="Google Photos commands")

console = Console()


# Common options


def album_options(func):
    """Album options. Use variables `max_albums`, `start_album`, `start_album_fresh`, and `album_ids` in your function."""
    func = click.option(
        "-m",
        "--max-albums",
        default=0,
        help="Maximum number of albums to processm, default: all albums",
    )(func)
    func = click.option(
        "-s",
        "--start-album",
        default=1,
        help="Start processing from this album position (1-based)",
    )(func)
    func = click.option(
        "-f",
        "--start-album-fresh",
        is_flag=True,
        help="Start processing from the beginning, ignoring existing albums",
    )(func)
    return func


def playwright_options(func):
    """Playwright options. Use variables `profile_dir` and `clear_storage` in your function."""
    func = click.option(
        "-p",
        "--profile-dir",
        envvar="PROFILE_DIR",
        show_envvar=True,
        default=str(playwright_session_dir),
        help="Path to store browser profile data",
    )(func)
    func = click.option(
        "-x",
        "--clear-storage",
        is_flag=True,
        help="Clear browser storage before starting",
    )(func)
    return func


# Common scraper setup
async def setup_scraper(
    db_path="immichporter.db",
    reset_db=False,
    log_level="warning",
    profile_dir=playwright_session_dir,
    max_albums=0,
    start_album=1,
    album_fresh=False,
    clear_storage=False,
):
    # Update database path
    global DATABASE_PATH
    DATABASE_PATH = db_path

    logger.info(f"Database path: {db_path}")

    # Create scraper instance
    scraper = GooglePhotosScraper(
        max_albums=max_albums,
        start_album=start_album,
        album_fresh=album_fresh,
        clear_storage=clear_storage,
        user_data_dir=profile_dir,
    )

    init_database(reset_db=reset_db)

    try:
        await scraper.setup_browser()
        return scraper
    except Exception as e:
        logger.error(f"Error setting up browser: {e}")
        await scraper.close()
        raise


@cli_gphotos.command()
@logging_options
@playwright_options
def login(log_level, clear_storage, profile_dir):
    """Login to Google Photos and save the session."""

    async def run_scraper_login():
        scraper = await setup_scraper(
            log_level=log_level,
            profile_dir=profile_dir,
            clear_storage=clear_storage,
        )

        try:
            await scraper.login()
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        finally:
            await scraper.close()

    asyncio.run(run_scraper_login())


@cli_gphotos.command()
@album_options
@database_options
@logging_options
@playwright_options
def albums(
    max_albums,
    start_album,
    start_album_fresh,
    db_path,
    reset_db,
    log_level,
    clear_storage,
    profile_dir,
):
    """List and export albums from Google Photos."""
    max_albums = max_albums if max_albums > 0 else 100000

    if start_album < 1:
        raise click.UsageError("Start album must be 1 or higher")

    async def run_scraper():
        scraper = await setup_scraper(
            db_path=db_path,
            reset_db=reset_db,
            log_level=log_level,
            profile_dir=profile_dir,
            max_albums=max_albums,
            start_album=start_album,
            album_fresh=start_album_fresh,
            clear_storage=clear_storage,
        )

        try:
            logger.info("Collecting albums...")
            albums = await scraper.collect_albums(
                max_albums=max_albums,
                start_album=start_album if not start_album_fresh else 1,
            )
            console.print(f"[green]Collected {len(albums)} albums[/green]")

            # Show database stats
            with get_db_session() as session:
                stats = get_database_stats(session)
                console.print("\n[bold green]=== Database Statistics ===[/bold green]")
                console.print(f"[green]Total albums: {stats['total_albums']}[/green]")
                console.print(f"[green]Total photos: {stats['total_photos']}[/green]")
                console.print(f"[green]Total users: {stats['total_users']}[/green]")
                console.print(f"[green]Total errors: {stats['total_errors']}[/green]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        finally:
            await scraper.close()

    asyncio.run(run_scraper())


@cli_gphotos.command()
@album_options
@click.option(
    "-a",
    "--album-id",
    type=int,
    multiple=True,
    help="Specific album ID to process (overrides max_albums and start_album)",
)
@click.option(
    "-n",
    "--not-finished",
    is_flag=True,
    help="Process only albums that have not been finished yet",
)
@database_options
@logging_options
@playwright_options
def photos(
    max_albums,
    start_album,
    start_album_fresh,
    album_id,
    not_finished,
    db_path,
    reset_db,
    log_level,
    clear_storage,
    profile_dir,
):
    """Export photos from Google Photos albums.

    By default, processes all albums. Use --album-id to process specific albums.
    """
    max_albums = max_albums if max_albums > 0 else None
    album_ids = album_id if album_id else None

    if not album_ids:  # Only validate start_album if not using album_ids
        if start_album < 1:
            raise click.UsageError("Start album must be 1 or higher")
    elif start_album_fresh or start_album > 1:
        console.print(
            "[yellow]Note: --start-album and --start-album-fresh are ignored when using --album-id[/yellow]"
        )

    async def run_scraper():
        scraper = await setup_scraper(
            db_path=db_path,
            reset_db=reset_db,
            log_level=log_level,
            profile_dir=profile_dir,
            max_albums=max_albums,
            start_album=start_album,
            album_fresh=start_album_fresh,
            clear_storage=clear_storage,
        )

        try:
            logger.info("Starting photo export for all albums...")
            await scraper.scrape_albums_from_db(
                max_albums=max_albums,
                start_album=start_album if not start_album_fresh else 1,
                album_ids=album_ids,
                not_finished=not_finished,
                skip_existing=not start_album_fresh,
            )

            # Show database stats
            with get_db_session() as session:
                stats = get_database_stats(session)
                console.print("\n[bold green]=== Export Complete ===[/bold green]")
                console.print(f"[green]Total albums: {stats['total_albums']}[/green]")
                console.print(f"[green]Total photos: {stats['total_photos']}[/green]")
                console.print(f"[green]Total errors: {stats['total_errors']}[/green]")

        except Exception as e:
            console.print(f"[red]Error during export: {e}[/red]")
            raise
        finally:
            await scraper.close()

    asyncio.run(run_scraper())
