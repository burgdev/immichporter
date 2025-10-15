"""Pydantic models for Immich API responses."""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AssetType(str, Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    OTHER = "OTHER"


class AssetResponse(BaseModel):
    """Represents an asset (photo/video) in Immich."""

    id: str
    device_asset_id: str = Field(..., alias="deviceAssetId")
    owner_id: str = Field(..., alias="ownerId")
    device_id: str = Field(..., alias="deviceId")
    type: AssetType
    original_path: str = Field(..., alias="originalPath")
    original_file_name: str = Field(..., alias="originalFileName")
    file_created_at: datetime = Field(..., alias="fileCreatedAt")
    file_modified_at: datetime = Field(..., alias="fileModifiedAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    is_favorite: bool = Field(..., alias="isFavorite")
    is_archived: bool = Field(..., alias="isArchived")
    duration: Optional[str] = None
    exif_info: Optional[Dict[str, Any]] = Field(None, alias="exifInfo")


class AlbumResponse(BaseModel):
    """Represents an album in Immich."""

    id: str
    album_name: str = Field(..., alias="albumName")
    description: Optional[str] = None
    album_thumbnail_asset_id: Optional[str] = Field(None, alias="albumThumbnailAssetId")
    shared: bool
    asset_count: int = Field(..., alias="assetCount")
    assets: List[AssetResponse] = []
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    album_thumbnail_asset: Optional[AssetResponse] = Field(
        None, alias="albumThumbnailAsset"
    )


class AlbumListResponse(BaseModel):
    """Response model for listing albums."""

    albums: List[AlbumResponse]
    count: int
