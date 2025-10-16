"""Database CLI commands."""

import click
import math
import json
from rich.console import Console
from rich.table import Table
from rich.text import Text
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from immichporter.models import User, Album, Photo, Error
from immichporter.database import Base, SessionLocal
from immichporter.database import (
    get_db_session,
    get_albums_from_db,
    get_users_from_db,
    get_database_stats,
    init_database,
)
from immichporter.utils import sanitize_for_email, format_csv_value
from immichporter.commands import logging_options
from ..gphotos.utils import traceback
from loguru import logger


cli_db = click.Group("db", help="Database commands")


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

    except (KeyboardInterrupt, EOFError) as e:
        click.echo("\nOperation cancelled", err=True)
        logger.debug(traceback(e))
        raise


console = Console()


@cli_db.command()
@logging_options
def init(log_level: str):
    """Initialize the database."""
    init_database()


@cli_db.command()
@logging_options
@click.option(
    "-n",
    "--not-finished",
    is_flag=True,
    help="Show only albums that are not fully processed",
)
def show_albums(not_finished, log_level: str):
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
                # title_text.append(" 🔗", style=Style(dim=True))

            table.add_row(
                str(album.album_id or "N/A"),
                title_text,
                str(album.items),
                f"{album.processed_items} [dim]{percentage_str}[/]",
                "Yes" if album.shared else "No",
                str(album.created_at)[:19] if album.created_at else "N/A",
            )

        console.print(table)


@cli_db.command()
@click.option(
    "-i",
    "--immich",
    is_flag=True,
    help="Show only users which are set to be added to immich",
)
@click.option("-p", "--show-password", is_flag=True, help="Show inital password")
@click.option(
    "-f",
    "--format",
    type=click.Choice(["table", "csv", "json"]),
    default="table",
    help="Output format",
)
@logging_options
def show_users(immich: bool, show_password: bool, format: str, log_level: str):
    """Show all users in the database."""
    with get_db_session() as session:
        users = get_users_from_db(session)

        if not users:
            console.print("[yellow]No users found in the database.[/yellow]")
            return

        if format == "table":
            table = Table(title="Users in Database")
            table.add_column("ID", style="cyan")
            table.add_column("Source Name", style="magenta")
            table.add_column("Immich Name", style="green")
            table.add_column("Email", style="yellow")
            table.add_column("Immich ID", style="cyan")
            table.add_column("Immich", style="green")
            if show_password:
                table.add_column("Initial Password", style="dim green")
            table.add_column("Created At", style="dim")
        else:
            table = []
            header = [
                "id",
                "source_name",
                "immich_name",
                "email",
                "immich_id",
                "immich",
            ]
            if show_password:
                header.append("initial_password")
            header.append("created_at")

        true_sign = "✓" if format == "table" else True
        false_sign = "✗" if format == "table" else False
        none_sign = "✗" if format == "table" else None

        for user in users:
            if immich:
                if not user.add_to_immich:
                    continue
            row = [
                str(user.id),
                f"[strike]{user.source_name}[/]"
                if not user.add_to_immich
                else user.source_name,
                user.immich_name or none_sign,
                user.immich_email or none_sign,
                str(user.immich_user_id)
                if user.immich_user_id is not None
                else none_sign,
                true_sign if user.add_to_immich else false_sign,
            ]
            if show_password:
                row.append(user.immich_initial_password or none_sign)
            row.append(str(user.created_at)[:19] if user.created_at else "N/A")
            if format == "table":
                table.add_row(*row)
            else:
                table.append(row)

        if format == "table":
            console.print(table)
        elif format == "csv":
            console.print(",".join(header))
            for row in table:
                click.echo(",".join(map(format_csv_value, row)))
        elif format == "json":
            table_json = [dict(zip(header, row)) for row in table]
            click.echo(json.dumps(table_json, indent=2))


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


@cli_db.command()
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
@logging_options
def edit_users(
    domain: str = None, all: bool = False, user_id: int = None, log_level: str = "INFO"
):
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


@cli_db.command()
@logging_options
def show_stats(log_level: str):
    """Show database statistics."""
    with get_db_session() as session:
        stats = get_database_stats(session)

        # Create a table for statistics
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Statistic", style="dim", width=30)
        table.add_column("Count", justify="right")

        # Add database stats
        table.add_row("Total Albums", str(stats["total_albums"]))
        table.add_row("Total Photos", str(stats["total_photos"]))
        table.add_row("Total Users", str(stats["total_users"]))
        table.add_row("Total Errors", str(stats["total_errors"]))

        # Add album stats if available
        if "album_stats" in stats:
            table.add_section()
            table.add_row("[bold]Album Statistics[/bold]", "")
            for album_name, count in stats["album_stats"].items():
                table.add_row(f"  {album_name}", str(count))

        # Add user stats if available
        if "user_stats" in stats:
            table.add_section()
            table.add_row("[bold]User Statistics[/bold]", "")
            for user_name, count in stats["user_stats"].items():
                table.add_row(f"  {user_name}", str(count))

        console.print(table)


def drop_table(name: str, all_tables: bool = False, force: bool = False):
    """Drop database tables or the entire database file.

    Args:
        name: Name of the table to drop (albums, photos, users, errors)
        all_tables: If True, drop all tables
        force: If True, don't ask for confirmation
    """
    if not any([name, all_tables]):
        console.print("[red]Error: Please specify a table name or use --all")
        return

    # Map table names to their models
    table_models = {"albums": Album, "photos": Photo, "users": User, "errors": Error}

    if all_tables:
        if not force:
            if not click.confirm(
                "Are you sure you want to drop ALL tables? This cannot be undone."
            ):
                console.print("Operation cancelled.")
                return

        with get_db_session() as session:
            try:
                # Drop all tables
                engine = SessionLocal().bind
                Base.metadata.drop_all(bind=engine)
                console.print("[green]All tables have been dropped.")

                # Recreate all tables
                Base.metadata.create_all(bind=engine)
                console.print("A new empty database has been initialized.")

            except Exception as e:
                console.print(f"[red]Error dropping tables: {str(e)}")
                logger.debug(traceback(e))
        return

    if name not in table_models:
        console.print(
            f"[red]Error: Invalid table name: {name}. Must be one of: {', '.join(table_models.keys())}"
        )
        return

    if not force:
        if not click.confirm(
            f"Are you sure you want to drop the '{name}' table? This cannot be undone."
        ):
            console.print("Operation cancelled.")
            return

    with get_db_session() as session:
        try:
            table = table_models[name].__table__

            # SQLite doesn't support CASCADE in DROP TABLE
            # First disable foreign key constraints
            session.execute(text("PRAGMA foreign_keys = OFF"))

            # If dropping albums, first delete all photos and errors that reference albums
            if name == "albums":
                session.execute(text("DELETE FROM photos"))
                session.execute(text("DELETE FROM errors"))

            # Drop the table
            session.execute(text(f"DROP TABLE IF EXISTS {table.name}"))

            # Re-enable foreign key constraints
            session.execute(text("PRAGMA foreign_keys = ON"))
            session.commit()

            console.print(f"[green]Table '{name}' has been dropped.")

            # Recreate the table
            engine = SessionLocal().bind
            Base.metadata.create_all(bind=engine, tables=[table])
            console.print(f"Table '{name}' has been recreated (empty).")

        except SQLAlchemyError as e:
            session.rollback()
            console.print(f"[red]Error dropping table: {str(e)}")
            logger.debug(traceback(e))
        except Exception as e:
            session.rollback()
            console.print(f"[red]Unexpected error: {str(e)}")
            logger.debug(traceback(e))


@cli_db.command("drop")
@click.option(
    "-n", "--name", help="Name of the table to drop (albums, photos, users, errors)"
)
@click.option(
    "-a",
    "--all",
    "all_tables",
    is_flag=True,
    help="Drop all tables and recreate the database",
)
@click.option("-f", "--force", "force", is_flag=True, help="Skip confirmation prompt")
@logging_options
@click.pass_context
def drop_command(ctx, name: str, all_tables: bool, force: bool, log_level: str):
    """Drop database tables or the entire database."""
    drop_table(name, all_tables, force)
