from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from uuid import UUID

from .models import Asset

from loguru import logger


class ImmichDBClient:
    """Minimal client for updating asset ownership in Immich database."""

    def __init__(self, database_url: str, echo: bool = False):
        """Initialize the database client.

        Args:
            database_url: Database connection URL (e.g., 'postgresql://user:password@localhost:5432/immich')
            echo: If True, log all SQL statements
        """
        self.engine = create_engine(database_url, echo=echo)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    @contextmanager
    def session_scope(self) -> Session:
        """Provide a transactional scope around operations."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            session.close()

    def update_asset_owner(self, asset_ids: List[str], new_owner_id: str) -> int:
        """Update the owner of multiple assets.

        Args:
            asset_ids: List of asset IDs to update
            new_owner_id: The new owner's UUID

        Returns:
            int: Number of assets updated
        """
        if not asset_ids:
            return 0

        try:
            new_owner_uuid = UUID(new_owner_id)
        except (ValueError, AttributeError):
            raise ValueError("Invalid owner_id format. Must be a valid UUID.")

        with self.session_scope() as session:
            result = (
                session.query(Asset)
                .filter(
                    Asset.id.in_(asset_ids),
                    Asset.owner_id
                    != new_owner_uuid,  # Only update if owner is different
                )
                .update({"ownerId": new_owner_uuid}, synchronize_session="fetch")
            )
            return result

    def count_assets_needing_owner_update(
        self, asset_ids: List[str], new_owner_id: str
    ) -> int:
        """Count how many assets need to be updated with the new owner.

        Args:
            asset_ids: List of asset IDs to check
            new_owner_id: The new owner's UUID to check against

        Returns:
            int: Number of assets that would be updated
        """
        if not asset_ids:
            return 0

        try:
            new_owner_uuid = UUID(new_owner_id)
        except (ValueError, AttributeError):
            raise ValueError("Invalid owner_id format. Must be a valid UUID.")

        with self.session_scope() as session:
            count = (
                session.query(Asset)
                .filter(Asset.id.in_(asset_ids), Asset.owner_id != new_owner_uuid)
                .count()
            )
            return count
