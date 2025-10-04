"""Schemas for album and photos."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class AlbumInfo:
    """Information about a Google Photos album."""

    title: str
    items: int
    shared: bool
    url: str
    album_id: int | None = None


@dataclass
class PictureInfo:
    """Information about a Google Photos picture."""

    filename: str
    date_taken: Optional[datetime]
    user: Optional[str]
    source_id: str


@dataclass
class ProcessingResult:
    """Data class for overall processing results."""

    total_albums: int
    total_pictures: int
    albums_processed: List[AlbumInfo]
    errors: List[str]


@dataclass
class ProcessingResult_error:
    """Data class for error information during processing."""

    error: str
    album_title: str = ""
    photo_url: str = ""
