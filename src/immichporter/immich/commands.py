"""Immich CLI commands."""

import asyncio
import click
import functools
import os
from loguru import logger
from immichporter.commands import logging_options
from rich.console import Console
from rich.table import Table
from typing import Optional

from immichporter.immich.client import ImmichAPI

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
        os.environ["IMMICH_ENDPOINT"] = kwargs["endpoint"]
        os.environ["IMMICH_API_KEY"] = kwargs["api_key"]
        os.environ["IMMICH_INSECURE"] = "1" if kwargs["insecure"] else "0"
        return f(*args, **kwargs)

    return wrapper


async def list_albums_function(limit: int = 50, shared: Optional[bool] = None):
    """List all albums on the Immich server.

    Args:
        endpoint: URL of the Immich server
        api_key: API key for authentication
        limit: Maximum number of albums to return
        shared: Filter by shared status (True for shared, False for not shared, None for all)
        insecure: If True, skip SSL certificate verification
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """

    endpoint = os.getenv("IMMICH_ENDPOINT")
    api_key = os.getenv("IMMICH_API_KEY")
    insecure = os.getenv("IMMICH_INSECURE") == "1"

    console.print(f"\n[bold]Fetching albums from {endpoint}...[/bold]")
    logger.info(f"Connecting to Immich server at {endpoint}")

    try:
        async with ImmichAPI(endpoint, api_key, verify_ssl=not insecure) as client:
            logger.info("Fetching albums...")
            albums = await client.get_all_albums()
            logger.info(f"Retrieved {len(albums) if albums else 0} albums")

            if not albums:
                console.print("[yellow]No albums found.[/yellow]")
                return

            # Filter by shared status if specified
            if shared is not None:
                albums = [a for a in albums if a.shared == shared]

            # Sort albums by name
            albums = sorted(albums, key=lambda x: x.album_name.lower())

            # Apply limit
            if limit > 0:
                albums = albums[:limit]

            # Create and display the table
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Album Name", style="cyan", no_wrap=True)
            table.add_column("ID", style="dim")
            table.add_column("Assets", justify="right")
            table.add_column("Shared", justify="center")
            table.add_column("Created At", style="dim")

            for album in albums:
                table.add_row(
                    album.album_name,
                    album.id,
                    str(album.asset_count),
                    "✓" if album.shared else "✗",
                    album.created_at.strftime("%Y-%m-%d"),
                )

            console.print(table)
            console.print(f"\n[green]Found {len(albums)} album(s)[/green]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise click.Abort()


# Add commands to the immich group
@cli_immich.command()
@immich_options
@click.option(
    "--limit", type=int, default=50, help="Maximum number of albums to return"
)
@click.option("--shared/--no-shared", default=None, help="Filter by shared status")
@logging_options
def list_albums(limit, shared, insecure, **options):
    """List all albums on the Immich server."""
    # configure_logging(log_level)
    return asyncio.run(
        list_albums_function(
            limit=limit,
            shared=shared,
        )
    )
