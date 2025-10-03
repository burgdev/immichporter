from tasks import info, error, success, warning, echo, env, task, header, Ctx, EnvError  # noqa: F401

import re
import sys

from typing import Literal


@task(
    default=True,
    help={
        "unreleased": "Get the unreleased, not published entries. Overwrites --version",
        "version": "Version to extract, either number or 'current' for the current version",
        "plain": "Do not print headers or warnings",
    },
)
def changelog(
    c: Ctx,
    unreleased: bool = False,
    version: str | Literal["current", "unreleased"] = "current",
    plain: bool = False,
):
    """Get changelog entries for a specific version"""
    if version == "unreleased" or unreleased:
        # get it from current PRs, not in CHANGELOG yet.
        content = c.run(
            "git-cliff --unreleased --bump --strip all | tail -n +2", hide=True
        ).stdout.strip()
        bumped_version = (
            c.run("git cliff --bumped-version", hide=True)
            .stdout.strip()
            .replace("v", "")
        )
        captured_version = f"latest: {bumped_version}"
    else:
        input_file = "CHANGELOG.md"

        try:
            with open(input_file, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            error(f"File {input_file} not found.")
        except Exception as e:
            error(f"An error occurred: {e}")

        # Initialize variables to capture the desired section
        capture = False
        extracted_content = []
        if version == "current":
            version_header_pattern = r"## \[(.*)\]\s+.*"
        else:
            version_header_pattern = rf"## \[({version})\]\s+.*"

        for line in lines:
            match = re.match(version_header_pattern, line)
            if match and not capture:
                captured_version = match.group(1)
                capture = True
                continue

            if capture:
                # Stop capturing if the next version is reached
                if re.match(r"^## \[.*\].*", line):
                    break
                extracted_content.append(line)
        content = "".join(extracted_content).strip().strip("\n")
    if not content:
        warning(f"Nothing found for '{version}'") if not plain else None
        sys.exit(1)
    else:
        header(f"Changelog for '{captured_version}'") if not plain else None
        echo(content, raw=True)
        header() if not plain else None
