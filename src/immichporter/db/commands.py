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
from immichporter.utils import sanitize_for_email


def prompt_with_default(text: str, default: str = None) -> str:
    """Prompt with a default value that can be edited using prompt_toolkit."""
    from prompt_toolkit import prompt
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.keys import Keys

    # For yes/no prompts with single character default
    if default in ("y", "n"):
        while True:
            try:
                click.echo(f"{text} (y/n) ", nl=False)
                char = click.getchar().lower()
                click.echo(char)  # Echo the character
                if char in ("y", "n"):
                    return char
                elif char in ("\r", "\n"):  # Enter
                    return default
            except (KeyboardInterrupt, EOFError):
                click.echo("\nOperation cancelled", err=True)
                raise

    # Create custom key bindings for editing
    kb = KeyBindings()

    @kb.add(Keys.Enter, eager=True)
    def _(event):
        """Accept the input."""
        event.current_buffer.validate_and_handle()

    try:
        # Show the prompt with the default value pre-filled and editable
        if default is not None:
            result = prompt(
                f"{text} ",
                default=default or "",
                key_bindings=kb,
            )
            return result if result.strip() else default
        else:
            return prompt(f"{text}: ")

    except (KeyboardInterrupt, EOFError):
        click.echo("\nOperation cancelled", err=True)
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
            console.print("[yellow]No users found in the database.[/yellow]")
            return

        table = Table(title="Users in Database")
        table.add_column("ID", style="cyan")
        table.add_column("Source Name", style="magenta")
        table.add_column("Immich Name", style="green")
        table.add_column("Email", style="yellow")
        table.add_column("Immich ID", style="cyan")
        table.add_column("Add to Immich", style="green")
        table.add_column("Created At", style="dim")

        for user in users:
            table.add_row(
                str(user.id),
                f"[strike]{user.source_name}[/]"
                if not user.add_to_immich
                else user.source_name,
                user.immich_name or "✗",
                user.immich_email or "✗",
                str(user.immich_user_id) if user.immich_user_id is not None else "✗",
                "✓" if user.add_to_immich else "✗",
                str(user.created_at)[:19] if user.created_at else "N/A",
            )

        console.print(table)


def update_user_immich_name(session: Session, user_id: int, immich_name: str) -> None:
    """Update a user's immich name."""
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.immich_name = immich_name or None
        session.commit()


def update_user_email(session: Session, user_id: int, email: str) -> None:
    """Update a user's email."""
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.immich_email = email or None
        session.commit()


def update_user_add_to_immich(
    session: Session, user_id: int, add_to_immich: bool
) -> None:
    """Update whether to include user in Immich imports."""
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.add_to_immich = add_to_immich
        session.commit()


@click.command()
@click.option(
    "-d",
    "--domain",
    type=str,
    default=None,
    help="Domain to use for email generation (e.g., example.com)",
)
@click.option(
    "-a",
    "--all",
    is_flag=True,
    default=False,
    help="Show all users, including those with email already set",
)
@click.option(
    "-u",
    "--user-id",
    type=int,
    help="Edit a specific user by ID",
)
def edit_users(domain: str = None, all: bool = False, user_id: int = None):
    """Interactively edit user information in the database.

    By default, only shows users added to Immich without an email.
    Use --all to show all users, or --user-id to edit a specific user.
    """

    with get_db_session() as session:
        if user_id is not None:
            # Edit specific user by ID
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                console.print(f"[red]User with ID {user_id} not found[/red]")
                return
            users = [user]
            all = True  # Show the user even if they have an email or are not added to Immich
        else:
            # Get all users
            users = get_users_from_db(session)
            if not users:
                console.print("[yellow]No users found in database[/yellow]")
                return

            # Filter users if --all is not set
            if not all:
                # Show only users added to Immich and without email by default
                filtered_users = [
                    u for u in users if u.add_to_immich and not u.immich_email
                ]
                if filtered_users:
                    users = filtered_users
                    console.print(
                        "[yellow]Showing only users added to Immich without email (use --all to show all users)[/yellow]"
                    )
                else:
                    users = []
                    console.print(
                        "[red]All users processed (use [yellow]--all[/yellow] to show all users)[/red]"
                    )

        # Always run in interactive mode
        for user in users:
            console.print("\n" + "─" * 50)
            console.print(
                f"User [cyan]{user.id}[/] - Source: [magenta]{user.source_name}[/]"
            )

            try:
                # Toggle add_to_immich
                current_status = "yes" if user.add_to_immich else "no"
                enable = prompt_with_default(
                    f"Include in Immich? [current: {current_status}]",
                    "y" if user.add_to_immich else "n",
                )

                if enable == "y":
                    # Edit name - use source_name as default if immich_name is not set
                    current_name = (
                        user.immich_name
                        if user.immich_name is not None
                        else user.source_name
                    )
                    new_name = prompt_with_default("  Immich name: ", current_name)
                    # If user enters a single dot, clear the name
                    if new_name.strip() == ".":
                        new_name = ""
                    if new_name != user.immich_name:
                        update_user_immich_name(
                            session, user.id, new_name if new_name.strip() else None
                        )
                        console.print(
                            f"  → Updated name to: [green]{new_name if new_name else '✗'}[/]"
                        )

                if enable.lower() == "y" or (enable == "" and user.add_to_immich):
                    # User is enabled for Immich
                    update_user_add_to_immich(session, user.id, True)

                    # Edit email
                    email_default = user.immich_email or ""

                    # Generate email proposal if domain is provided
                    if domain and not email_default:
                        # Use the current immich_name (which might have just been updated) or source_name
                        name_to_use = user.immich_name or user.source_name
                        email_local = sanitize_for_email(name_to_use)
                        email_default = f"{email_local}@{domain}"

                    new_email = prompt_with_default("  Email: ", email_default)
                    if new_email != user.immich_email:
                        update_user_email(session, user.id, new_email)
                        console.print(f"  → Updated email to: [yellow]{new_email}[/]")

                elif enable.lower() == "n" or (enable == "" and not user.add_to_immich):
                    # User is disabled for Immich
                    update_user_add_to_immich(session, user.id, False)
                    if user.immich_name:
                        update_user_immich_name(session, user.id, None)
                    console.print("  [yellow]User disabled for Immich import[/]")

                # Add a small space between users
                console.print()

            except (KeyboardInterrupt, EOFError):
                if click.confirm("\nDo you want to stop editing?"):
                    break
                continue

        console.print(
            "Run [yellow]'immichporter db show-users'[/yellow] to see the updated users."
        )
        # show_users.callback()


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
