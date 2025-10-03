"""Google Photos CLI commands."""

import asyncio
import click
from rich.console import Console

from immichporter.database import get_db_session, get_database_stats
from immichporter.gphotos.scraper import GooglePhotosScraper, USER_DATA_DIR

# Create a Click command group
gphoto = click.Group("gphoto", help="Google Photos commands")

console = Console()


# Common options
def common_options(func):
    func = click.option(
        "--db-path", default="photos.db", help="Path to the SQLite database file"
    )(func)
    func = click.option(
        "--log-level",
        type=click.Choice(["debug", "info", "warning", "error"]),
        default="warning",
        help="Set the logging level",
    )(func)
    return func


def configure_logging(log_level):
    from loguru import logger

    logger.remove()
    logger.add(
        lambda msg: print(msg, end=""),
        level=log_level.upper(),
        format="<green>{time:HH:mm:ss}</green> <level>{level: <8}</level><level>{message}</level>",
        colorize=True,
    )
    console.print(f"[blue]Logging level set to: {log_level}[/blue]")


# Common scraper setup
async def setup_scraper(
    db_path="photos.db",
    log_level="warning",
    user_data_dir=USER_DATA_DIR,
    clear_storage=False,
):
    # Update database path
    global DATABASE_PATH
    DATABASE_PATH = db_path

    # Configure logging
    configure_logging(log_level)
    console.print(f"[blue]Database path: {db_path}[/blue]")
    # console.print(f"[blue]Chrome binary: {BRAVE_EXECUTABLE}[/blue]")

    # Create scraper instance
    scraper = GooglePhotosScraper(
        clear_storage=clear_storage, user_data_dir=user_data_dir
    )

    try:
        await scraper.setup_browser()
        return scraper
    except Exception as e:
        console.print(f"[red]Error setting up browser: {e}[/red]")
        await scraper.close()
        raise


@gphoto.command()
@click.option(
    "-m", "--max-albums", default=0, help="Maximum number of albums to process"
)
@click.option(
    "-s",
    "--start-album",
    default=1,
    help="Start processing from this album position (1-based)",
)
@click.option(
    "-f",
    "--start-album-fresh",
    is_flag=True,
    help="Start processing from the beginning, ignoring existing albums",
)
@click.option(
    "-x", "--clear-storage", is_flag=True, help="Clear browser storage before starting"
)
@common_options
def albums(
    max_albums, start_album, start_album_fresh, clear_storage, db_path, log_level
):
    """List and export albums from Google Photos."""
    max_albums = max_albums if max_albums > 0 else 100000

    if start_album < 1:
        raise click.UsageError("Start album must be 1 or higher")

    async def run_scraper():
        user_data_dir = USER_DATA_DIR
        scraper = await setup_scraper(
            db_path=db_path,
            log_level=log_level,
            user_data_dir=user_data_dir,
            clear_storage=clear_storage,
        )

        try:
            console.print("[green]Collecting albums...[/green]")
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


@click.command()
@click.option(
    "--max-albums",
    type=int,
    default=0,
    help="Maximum number of albums to process (0 for all)",
)
@click.option(
    "--start-album", type=int, default=1, help="Start processing from this album number"
)
@click.option(
    "--clear-storage", is_flag=True, help="Clear browser storage before starting"
)
@click.option(
    "--user-data-dir",
    default="./brave_playwright_profile",
    help="Path to store browser profile data",
)
@click.option("--db-path", default="photos.db", help="Path to the SQLite database file")
@click.option(
    "--log-level",
    type=click.Choice(["debug", "info", "warning", "error"]),
    default="warning",
    help="Set the logging level",
)
def photos(max_albums, start_album, clear_storage, user_data_dir, db_path, log_level):
    """Export photos from Google Photos albums."""

    async def run_scraper():
        scraper = await setup_scraper(
            db_path=db_path,
            log_level=log_level,
            user_data_dir=user_data_dir,
            clear_storage=clear_storage,
        )

        try:
            console.print("[green]Starting photo export...[/green]")
            await scraper.scrape_albums_from_db(
                max_albums=max_albums, start_album=start_album
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


@click.command()
@click.option(
    "--clear-storage", is_flag=True, help="Clear browser storage before starting"
)
@click.option(
    "--user-data-dir", default=USER_DATA_DIR, help="Path to store browser profile data"
)
@click.option("--db-path", default="photos.db", help="Path to the SQLite database file")
@click.option(
    "--log-level",
    type=click.Choice(["debug", "info", "warning", "error"]),
    default="warning",
    help="Set the logging level",
)
def login(clear_storage, user_data_dir, db_path, log_level):
    """Log in to Google Photos and save the session."""

    async def run_scraper_login():
        user_data_dir = USER_DATA_DIR
        scraper = await setup_scraper(
            log_level=log_level,
            user_data_dir=user_data_dir,
            clear_storage=clear_storage,
        )

        try:
            await scraper.login()
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        finally:
            await scraper.close()

    asyncio.run(run_scraper_login())


# Register commands
gphoto.add_command(login)
gphoto.add_command(albums)
gphoto.add_command(photos)
