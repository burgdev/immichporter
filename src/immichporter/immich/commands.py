"""Immich CLI commands."""

import click
import functools
from loguru import logger
from immichporter.commands import logging_options
from rich.console import Console
from rich.table import Table

from immichporter.immich.immich import ImmichClient, immich_api_client

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

        console.print(table)
        return albums

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        logger.exception("Failed to fetch albums")
        raise click.Abort()
