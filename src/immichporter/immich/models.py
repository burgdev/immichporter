"""Immich specific models and dataclasses."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ImmichAlbum:
    """Information about an Immich album."""

    id: str
    name: str
    asset_count: int
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class ImmichAsset:
    """Information about an Immich asset."""

    id: str
    original_filename: str
    device_asset_id: str
    device_id: str
    type: str  # 'IMAGE', 'VIDEO', etc.
    file_size: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class ImmichUser:
    """Information about an Immich user."""

    id: str
    name: str
    email: str
    avatar_color: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
