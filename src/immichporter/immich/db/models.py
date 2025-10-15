from enum import Enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AssetStatus(str, Enum):
    """Status of an asset in Immich."""

    NOT_VISIBLE = "NOT_VISIBLE"
    VISIBLE = "VISIBLE"
    ARCHIVED = "ARCHIVED"
    TRASHED = "TRASHED"


class AssetVisibility(str, Enum):
    """Visibility of an asset in Immich."""

    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    SHARED = "SHARED"


class Asset(Base):
    """Asset model for Immich database."""

    __tablename__ = "asset"

    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    owner_id = Column("ownerId", PG_UUID(as_uuid=True), nullable=False)
    device_asset_id = Column("deviceAssetId", String, nullable=False)
    original_file_name = Column("originalFileName", String, nullable=False)
    file_created_at = Column("fileCreatedAt", DateTime, nullable=False)
    file_modified_at = Column("fileModifiedAt", DateTime, nullable=False)
    status = Column(SQLAEnum(AssetStatus), nullable=False)
    visibility = Column(SQLAEnum(AssetVisibility), nullable=False)
    created_at = Column("createdAt", DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        "updatedAt",
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
