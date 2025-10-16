"""Schemas for album and photos."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class AlbumInfo:
    """Information about a Google Photos album.

    Attributes:
        title: The title of the album
        items: Total number of items in the album
        shared: Whether the album is shared
        url: URL of the album
        album_id: Internal database ID of the album
        processed_items: Number of items that have been processed
        created_at: When the album was created in the database
    """

    title: str
    items: int
    shared: bool
    url: str
    album_id: int | None = None
    processed_items: int = 0
    created_at: str | None = None


@dataclass
class PictureInfo:
    """Information about a Google Photos picture."""

    filename: str
    date_taken: Optional[datetime]
    user: Optional[str]
    source_id: str
    user_id: int | None = None


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
