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
    """Immichporter - Import photos from various sources to Immich."""
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
        console.print("[dim]use -l debug to see traceback[/dim]")
        sys.exit(1)
        # sys.__excepthook__(exc_type, exc_value, exc_traceback)


sys.excepthook = handle_keyboard_interrupt


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
