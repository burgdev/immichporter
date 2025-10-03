from rich import print as rprint
import sys
from environs import Env
import inspect
import shutil

env = Env()
env.read_env()  # read .env file, if it exists


def echo(*args, raw=False, **kwargs):
    if raw:
        print(*args, **kwargs)
    else:
        rprint(*args, **kwargs)


def header(
    msg: str = "", symb="-", style="blue bold", max_length=None, stderr: bool = True
):
    terminal_width = shutil.get_terminal_size(fallback=(80, 20)).columns
    max_length = int(terminal_width)
    max_length = 50 if max_length < 50 else 120 if max_length > 120 else max_length
    min_ = 6
    max_ = max_length - min_ - 2
    length = len(msg)
    start = f"[dim]{symb * (max_ - length) if length < max_ else symb * min_}[/]"
    end = f"[dim]{symb*min_}[/]"
    if not msg:
        echo(f"[dim]{symb*max_length}[/]", file=sys.stderr if stderr else None)
    else:
        echo(f"{start} [{style}]{msg} {end}", file=sys.stderr if stderr else None)


def info(msg: str, stderr: bool = True):
    echo("[blue]Info   :[/]", msg, file=sys.stderr if stderr else None)


def success(msg: str, stderr: bool = True):
    echo("[green bold]Success:[/]", msg, file=sys.stderr if stderr else None)


def warning(msg: str, stderr: bool = True):
    echo("[yellow]Warning:[/]", msg, file=sys.stderr if stderr else None)


def error(msg: str, stderr: bool = True):
    echo(f"[red bold]Error:  [/] [red]{msg}[/]", file=sys.stderr if stderr else None)
    sys.exit(1)


def doc():
    """Retrieve and print the docstring of the caller function."""
    caller_frame = inspect.stack()[1]
    caller = caller_frame.frame.f_globals.get(caller_frame.function)
    return inspect.getdoc(caller) or ""
