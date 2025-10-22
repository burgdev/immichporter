"""Main CLI entry point for immichporter package."""

import click
import sys

# Import subcommands
from immichporter.gphotos.commands import cli_gphotos
from immichporter.db.commands import cli_db
from immichporter.immich.commands import cli_immich

from loguru import logger
from rich.console import Console
from immichporter.gphotos.utils import traceback

console = Console()


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option()
def cli():
    """Immichporter retrieves metadata not available in google takeout,
    including shared albums, assets, and shared users.
    You can use this data to update assets in Immich,
    re-add users to shared albums, and even move assets to their correct owners.

    The command line interface uses subcommands for the various tasks (see below).

    This are the steps needed to extract the information from google photos and update immich:

    \b
        immich-go ... # see https://github.com/simulot/immich-go
        immichporter gphotos login
        immichporter gphotos albums
        immichporter gphotos photos
        immichporter db edit-users
        export IMMICH_ENDPOINT=http://localhost:2283
        export IMMICH_API_KEY=your_api_key
        export IMMICH_INSECURE=1
        immichporter immich update-users
        immichporter immich update-albums
        immichporter immich sync-albums
        immichporter immich adjust-owners

    """
    pass


cli.add_command(cli_gphotos)
cli.add_command(cli_db)
cli.add_command(cli_immich)


def handle_keyboard_interrupt(exc_type, exc_value, exc_traceback):
    if exc_type is KeyboardInterrupt:
        console.print("[red]Abort[/red]")
        logger.debug(traceback(exc_value))
        sys.exit(1)
    else:
        logger.debug(traceback(exc_value))
        console.print("[red]Exception [dim]" + str(exc_value) + "[/]")
        console.print(
            "[dim]Use [i][yellow]-l debug[/yellow][/i] to see traceback[/dim]"
        )
        sys.exit(1)
        # sys.__excepthook__(exc_type, exc_value, exc_traceback)


sys.excepthook = handle_keyboard_interrupt


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
