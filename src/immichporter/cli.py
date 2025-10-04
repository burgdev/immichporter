"""Main CLI entry point for immichporter package."""

import click
from rich.console import Console

# Import subcommands
from immichporter.gphotos.commands import login, albums, photos
from immichporter.db.commands import (
    show_albums,
    show_users,
    show_stats,
    init,
    edit_users,
    drop_command,
)
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


# Register Google Photos commands
gphotos.add_command(login)
gphotos.add_command(albums)
gphotos.add_command(photos)

# Register database commands
db.add_command(show_albums, name="show-albums")
db.add_command(show_users, name="show-users")
db.add_command(show_stats, name="show-stats")
db.add_command(init)
db.add_command(edit_users, name="edit-users")
db.add_command(drop_command, name="drop")

# Register Immich commands
immich.add_command(create_album, name="create-album")
immich.add_command(import_photos, name="import-photos")


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
