"""Database CLI commands."""

import click
import math
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.style import Style
from sqlalchemy.orm import Session
from immichporter.models import User
from immichporter.database import (
    get_db_session,
    get_albums_from_db,
    get_users_from_db,
    get_database_stats,
    init_database,
)


def prompt_with_default(text: str, default: str) -> str:
    """Prompt with a default value that can be edited using prompt_toolkit."""
    from prompt_toolkit import prompt
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.keys import Keys

    # Create custom key bindings
    kb = KeyBindings()

    @kb.add(Keys.Enter, eager=True)
    def _(event):
        """Accept the input."""
        event.current_buffer.validate_and_handle()

    try:
        # Show the prompt with the default value pre-filled
        result = prompt(
            f"{text} ",
            default=default,
            key_bindings=kb,
            pre_run=lambda: None,  # This is a workaround for prompt_toolkit
        )
        return result if result.strip() else default
    except (KeyboardInterrupt, EOFError):
        console.print("\n[red]Operation cancelled[/red]")
        raise


console = Console()


@click.command()
def init():
    """Initialize the database."""
    init_database()


@click.command()
@click.option(
    "-n",
    "--not-finished",
    is_flag=True,
    help="Show only albums that are not fully processed",
)
def show_albums(not_finished):
    """Show albums in the database."""
    with get_db_session() as session:
        albums = get_albums_from_db(session, not_finished=not_finished)

        if not albums:
            msg = "No albums found"
            if not_finished:
                msg += " that are not fully processed"
            console.print(f"[yellow]{msg} in database[/yellow]")
            return

        table_title = "Albums"
        if not_finished:
            table_title += " (Not Fully Processed)"

        table = Table(title=table_title)
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="magenta")
        table.add_column("Items", style="green")
        table.add_column("Processed", style="yellow")
        table.add_column("Shared", style="red")
        table.add_column("Created", style="dim")

        for album in albums:
            # Calculate percentage with floor to avoid showing 100% until fully processed
            percentage = (
                math.floor((album.processed_items / album.items) * 100)
                if album.items > 0
                else 0
            )
            percentage_str = f"({percentage}%)"

            # Create clickable title with URL if available
            title_text = Text(album.title)
            if hasattr(album, "url") and album.url:
                title_text.stylize(f"link {album.url}")
                title_text.append(" 🔗", style=Style(dim=True))

            table.add_row(
                str(album.album_id or "N/A"),
                title_text,
                str(album.items),
                f"{album.processed_items} [dim]{percentage_str}[/]",
                "Yes" if album.shared else "No",
                str(album.created_at)[:19] if album.created_at else "N/A",
            )

        console.print(table)


@click.command()
def show_users():
    """Show all users in the database."""
    with get_db_session() as session:
        users = get_users_from_db(session)

        if not users:
            return

        table = Table(title="Users")
        table.add_column("ID", style="cyan")
        table.add_column("Source Name", style="magenta")
        table.add_column("Immich Name", style="green")
        table.add_column("Source Type", style="blue")
        table.add_column("Email", style="yellow")
        table.add_column("Created", style="dim")

        for user in users:
            table.add_row(
                str(user.id),
                user.source_name,
                user.immich_name or "[dim]Not set[/]",
                user.source_type,
                user.immich_email or "[dim]Not set[/]",
                str(user.created_at)[:19],
            )

        console.print(table)


def update_user_immich_name(session: Session, user_id: int, immich_name: str) -> None:
    """Update a user's immich name."""
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.immich_name = immich_name or None
        session.commit()


@click.command()
@click.option(
    "--use-source-name",
    is_flag=True,
    help="Copy source name to immich name for all users",
)
@click.option(
    "--interactive",
    is_flag=True,
    help="Interactively edit each user's immich name",
)
def edit_users(use_source_name: bool, interactive: bool):
    """Edit user information in the database.

    At least one of --use-source-name or --interactive must be provided.
    """
    if not (use_source_name or interactive):
        console.print(
            "[red]Error: At least one of --use-source-name or --interactive must be provided[/red]"
        )
        return

    with get_db_session() as session:
        users = get_users_from_db(session)
        if not users:
            console.print("[yellow]No users found in database[/yellow]")
            return

        if use_source_name:
            console.print("\n[bold]Updating immich names from source names...[/]")
            for user in users:
                if not user.immich_name or user.immich_name != user.source_name:
                    console.print(
                        f"  - [cyan]{user.source_name}[/] -> [green]{user.source_name}[/]"
                    )
                    update_user_immich_name(session, user.id, user.source_name)
            console.print("[green]✓ Done updating immich names[/]")

        if interactive:
            console.print("\n[bold]Interactive mode:[/]")
            for user in users:
                current = user.immich_name or user.source_name
                # Show current name as pre-filled text that can be edited
                console.print(
                    f"\nUser [cyan]{user.id}[/] - Source: [magenta]{user.source_name}[/]"
                )
                try:
                    new_name = prompt_with_default("Immich name: ", current)
                except (KeyboardInterrupt, EOFError):
                    return
                if new_name.strip() and new_name != user.immich_name:
                    update_user_immich_name(session, user.id, new_name)
                    console.print(f"  → Updated to: [green]{new_name}[/]")
                else:
                    console.print("  [dim]No changes made[/]")

        console.print("\n[bold]Updated users:[/]")
        show_users.callback()


@click.command()
def show_stats():
    """Show database statistics."""
    with get_db_session() as session:
        stats = get_database_stats(session)

        console.print("[bold green]Database Statistics[/bold green]")
        console.print(f"Total Albums: {len(stats['albums'])}")
        console.print(f"Total Users: {stats['user_count']}")
        console.print(f"Total Photos: {stats['total_photos']}")
        console.print(f"Total Errors: {stats['total_errors']}")

        if stats["albums"]:
            console.print("\n[bold blue]Album Details[/bold blue]")
            table = Table()
            table.add_column("Album", style="magenta")
            table.add_column("Type", style="blue")
            table.add_column("Items", style="green")
            table.add_column("Photos", style="yellow")
            table.add_column("Errors", style="red")

            for album_stat in stats["albums"]:
                table.add_row(
                    album_stat.source_title,
                    album_stat.source_type,
                    str(album_stat.items),
                    str(album_stat.photo_count),
                    str(album_stat.error_count),
                )

            console.print(table)
