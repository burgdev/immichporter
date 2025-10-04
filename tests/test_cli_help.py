"""Test that all CLI commands can be called with --help."""

import pytest
from click.testing import CliRunner

from immichporter.cli import cli

# List of all commands to test
COMMANDS = [
    ("main", []),
    ("version", ["--version"]),
    ("gphotos", ["gphotos", "--help"]),
    ("gphotos_login", ["gphotos", "login", "--help"]),
    ("gphotos_albums", ["gphotos", "albums", "--help"]),
    ("gphotos_photos", ["gphotos", "photos", "--help"]),
    ("db", ["db", "--help"]),
    ("db_drop", ["db", "drop", "--help"]),
    ("db_show_albums", ["db", "show-albums", "--help"]),
    ("db_show_users", ["db", "show-users", "--help"]),
    ("db_edit_users", ["db", "edit-users", "--help"]),
    ("db_show_stats", ["db", "show-stats", "--help"]),
    ("db_init", ["db", "init", "--help"]),
    ("immich", ["immich", "--help"]),
    ("immich_create_album", ["immich", "create-album", "--help"]),
    ("immich_import_photos", ["immich", "import-photos", "--help"]),
]


@pytest.mark.parametrize("name,cmd_args", COMMANDS)
def test_cli_help(name, cmd_args):
    """Test that all commands can be called with --help."""
    runner = CliRunner()
    # Only add --help if it's not already in the command
    if "--help" not in " ".join(cmd_args) and "--version" not in " ".join(cmd_args):
        cmd_args = cmd_args + ["--help"]

    result = runner.invoke(cli, cmd_args, catch_exceptions=True)

    # For debugging
    if result.exception:
        print(f"\nError in {name}:")
        print(f"Command: {' '.join(cmd_args)}")
        print(f"Exception: {result.exception}")
        print(f"Output: {result.output}")

    assert (
        result.exit_code == 0
    ), f"Command failed: {name} - {' '.join(cmd_args)}\n{result.output}"
