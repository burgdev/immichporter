"""Main CLI entry point for immichporter package."""

import click

# Import subcommands
from immichporter.gphotos.commands import cli_gphotos
from immichporter.db.commands import cli_db
from immichporter.immich.commands import cli_immich


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option()
def cli():
    """Immichporter - Import photos from various sources to Immich."""
    pass


cli.add_command(cli_gphotos)
cli.add_command(cli_db)
cli.add_command(cli_immich)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
