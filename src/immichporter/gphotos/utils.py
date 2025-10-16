"""Google Photos specific utilities."""

import re
from typing import Optional
from datetime import datetime

from io import StringIO
from rich.console import Console
from rich.traceback import Traceback


def traceback(e: Exception) -> str:
    buffer = StringIO()
    console = Console(file=buffer, force_terminal=True)
    tb = Traceback.from_exception(type(e), e, e.__traceback__)
    console.print(tb)
    return "...\n" + buffer.getvalue()


def parse_date_from_filename(filename: str) -> Optional[datetime]:
    """Parse date from Google Photos filename format."""
    # Google Photos filename format: IMG_YYYYMMDD_HHMMSS.jpg
    match = re.search(r"IMG_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})", filename)
    if match:
        year, month, day, hour, minute, second = match.groups()
        try:
            return datetime(
                int(year), int(month), int(day), int(hour), int(minute), int(second)
            )
        except ValueError:
            return None
    return None


def clean_filename(filename: str) -> str:
    """Clean filename for filesystem compatibility."""
    # Remove problematic characters
    cleaned = re.sub(r'[<>:"/\\|?*]', "", filename)
    # Replace multiple spaces with single space
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def extract_user_from_filename(filename: str) -> Optional[str]:
    """Extract user name from filename if present."""
    # Some Google Photos filenames include user info
    match = re.search(r"from_([^_]+)", filename)
    if match:
        return match.group(1)
    return None
