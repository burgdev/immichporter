"""Google Photos CLI commands."""

import click
from rich.console import Console

from loguru import logger

import functools

console = Console()


# Common options
def database_options(func):
    """Database options. Use variable `db_path` and `reset_db` in your function."""
    func = click.option(
        "--db-path",
        default="immichporter.db",
        help="Path to the SQLite database file",
        envvar="DB_PATH",
        show_envvar=True,
        show_default=True,
    )(func)
    func = click.option(
        "-r",
        "--reset-db",
        help="Reset the database",
        is_flag=True,
    )(func)
    return func


def logging_options(f):
    """Common options for Immich commands."""

    @click.option(
        "-l",
        "--log-level",
        envvar="LOG_LEVEL",
        show_envvar=True,
        type=click.Choice(["debug", "info", "warning", "error"]),
        default="warning",
        help="Set the logging level",
    )
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        configure_logging(kwargs["log_level"])
        return f(*args, **kwargs)

    return wrapper


def configure_logging(log_level):
    logger.remove()
    logger.add(
        lambda msg: print(msg, end=""),
        level=log_level.upper(),
        format="<green>{time:HH:mm:ss}</green> <level>{level: <8}</level>{message}",
        colorize=True,
    )
    logger.info(f"Logging level set to: {log_level}")
