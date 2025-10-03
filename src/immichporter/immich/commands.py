"""Immich CLI commands."""

import click
from rich.console import Console
from immichporter.database import get_db_session, get_database_stats

console = Console()


@click.command()
def create_album():
    """Create albums in Immich from database."""
    console.print("[yellow]Immich album creation not yet implemented[/yellow]")
    console.print("[blue]This will require Immich API integration[/blue]")

    # Show current database stats
    with get_db_session() as session:
        stats = get_database_stats(session)
        console.print("\n[green]Current database stats:[/green]")
        console.print(f"  Albums: {len(stats['albums'])}")
        console.print(f"  Users: {stats['user_count']}")
        console.print(f"  Photos: {stats['total_photos']}")
        console.print(f"  Errors: {stats['total_errors']}")


@click.command()
def import_photos():
    """Import photos to Immich from database."""
    console.print("[yellow]Immich photo import not yet implemented[/yellow]")
    console.print("[blue]This will require Immich API integration[/blue]")

    # Show current database stats
    with get_db_session() as session:
        stats = get_database_stats(session)
        console.print("\n[green]Current database stats:[/green]")
        console.print(f"  Albums: {len(stats['albums'])}")
        console.print(f"  Users: {stats['user_count']}")
        console.print(f"  Photos: {stats['total_photos']}")
        console.print(f"  Errors: {stats['total_errors']}")
