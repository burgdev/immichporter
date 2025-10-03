"""Main CLI entry point for immichporter package."""

import click
from rich.console import Console

# Import subcommands
from immichporter.gphotos.commands import login, albums, photos
from immichporter.db.commands import show_albums, show_users, show_stats, init
from immichporter.immich.commands import create_album, import_photos

console = Console()


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option()
def cli():
    """Immichporter - Import photos from various sources to Immich."""
    pass


@cli.group()
def gphotos():
    """Google Photos source operations."""
    pass


@cli.group()
def db():
    """Database operations."""
    pass


@cli.group()
def immich():
    """Immich target operations."""
    pass


# Register subcommands
gphotos.add_command(login)
gphotos.add_command(albums)
gphotos.add_command(photos)


# Register other commands
db.add_command(show_albums)
db.add_command(show_users)
db.add_command(show_stats)
db.add_command(init)
immich.add_command(create_album)
immich.add_command(import_photos)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
