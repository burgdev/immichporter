"""Database operations for immichporter."""

from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List, Dict, Any, Optional
from rich.console import Console
from loguru import logger

from immichporter.models import Base, Album, User, Photo, Error, AlbumUser, SessionLocal

from immichporter.schemas import AlbumInfo, PictureInfo

console = Console()

# Module-level variable to track if database has been initialized
_database_initialized = False


def get_db_session() -> Session:
    """Get a database session. Initializes and migrates the database if needed."""
    global _database_initialized
    if not _database_initialized:
        # Initialize the database only once per session
        init_database()
        _database_initialized = True
    return SessionLocal()


def init_database(reset_db: bool = False) -> None:
    """Initialize the database and apply any necessary migrations."""
    from sqlalchemy import inspect, text

    engine = SessionLocal().bind

    if reset_db:
        Base.metadata.drop_all(bind=engine)

    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Apply migrations
    inspector = inspect(engine)

    # Migration 1: Add add_to_immich column if it doesn't exist
    if "users" in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns("users")]
        if "add_to_immich" not in columns:
            with engine.begin() as conn:
                conn.execute(
                    text(
                        "ALTER TABLE users ADD COLUMN add_to_immich BOOLEAN DEFAULT TRUE NOT NULL"
                    )
                )
                console.print(
                    "[yellow]Applied migration: Added add_to_immich column to users table[/yellow]"
                )

        # Migration 2: Add immich_user_id column if it doesn't exist
        if "immich_user_id" not in columns:
            with engine.begin() as conn:
                conn.execute(
                    text("ALTER TABLE users ADD COLUMN immich_user_id INTEGER")
                )
                console.print(
                    "[yellow]Applied migration: Added immich_user_id column to users table[/yellow]"
                )
        if "immich_initial_password" not in columns:
            with engine.begin() as conn:
                conn.execute(
                    text("ALTER TABLE users ADD COLUMN immich_initial_password STRING")
                )

    if "photos" in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns("photos")]
        if "immich_id" not in columns:
            with engine.begin() as conn:
                conn.execute(text("ALTER TABLE photos ADD COLUMN immich_id STRING"))
                console.print(
                    "[yellow]Applied migration: Added immich_id column to photos table[/yellow]"
                )

    # Migration: Add immich_id to albums table
    if "albums" in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns("albums")]
        if "immich_id" not in columns:
            with engine.begin() as conn:
                conn.execute(text("ALTER TABLE albums ADD COLUMN immich_id STRING"))
                console.print(
                    "[yellow]Applied migration: Added immich_id column to albums table[/yellow]"
                )

    logger.debug("Database initialized and migrated successfully")


def insert_or_update_album(session: Session, album_info) -> int:
    """Insert or update an album from AlbumInfo object."""
    # Check if album exists
    existing_album = (
        session.query(Album)
        .filter_by(source_url=album_info.url, source_type="gphoto")
        .first()
    )

    if existing_album:
        # Update existing album
        existing_album.items = album_info.items
        existing_album.shared = album_info.shared
        existing_album.source_url = album_info.url
        console.print(f"[yellow]Updated album: {album_info.title}[/yellow]")
        session.commit()
        return existing_album.id
    else:
        # Insert new album
        album = Album(
            source_title=album_info.title,
            source_type="gphoto",
            immich_title=album_info.title,
            items=album_info.items,
            shared=album_info.shared,
            source_url=album_info.url,
        )
        session.add(album)
        session.commit()
        console.print(f"[green]Added album: {album_info.title}[/green]")
        return album.id


def insert_or_update_user(
    session: Session, user_name: str, add_to_immich: bool = True
) -> int:
    """Insert or update a user.

    Args:
        session: Database session
        user_name: Name of the user in the source system
        add_to_immich: Whether to include this user in Immich imports (default: True)
    """
    # Check if user exists
    existing_user = (
        session.query(User)
        .filter_by(source_name=user_name, source_type="gphoto")
        .first()
    )

    if existing_user:
        logger.debug(f"User already exists: {user_name}")
        return existing_user.id
    else:
        # Insert new user
        user = User(
            source_name=user_name, source_type="gphoto", add_to_immich=add_to_immich
        )
        session.add(user)
        session.commit()
        logger.info(f"Added user: {user_name} (add_to_immich={add_to_immich})")
        return user.id


def insert_photo(
    session: Session, picture_info: PictureInfo, album_id: int, update: bool = False
) -> tuple[bool | None, int | None]:
    """Insert a photo, returning a tuple (updated, photo_id | None), updated is None if photo was not inserted.

    Returns:
        A tuple (update, photo_id | None)
    """
    logger.debug(f"Inserting photo: {picture_info}")
    # Check if photo already exists
    existing_photo = (
        session.query(Photo)
        .filter_by(source_id=picture_info.source_id, album_id=album_id)
        .first()
    )

    if existing_photo and not update:
        logger.info(f"Photo already exists: {picture_info.filename} (not updated)")
        return None, existing_photo.id
    elif existing_photo:  # update
        something_changed = False
        for attr in ["filename", "date_taken", "user_id", "source_id"]:
            if getattr(picture_info, attr) != getattr(existing_photo, attr):
                if something_changed is False:
                    logger.info(
                        f"Photo #{existing_photo.id} '{picture_info.filename}' updates:"
                    )
                if attr == "user_id":
                    user_name = picture_info.user
                    logger.info(
                        f"  - {f'{attr}:':<15} from '{getattr(existing_photo, attr)}' to '{getattr(picture_info, attr)}' ({user_name})"
                    )
                else:
                    logger.info(
                        f"  - {f'{attr}:':<15} from '{getattr(existing_photo, attr)}' to '{getattr(picture_info, attr)}'"
                    )
                setattr(existing_photo, attr, getattr(picture_info, attr))
                something_changed = True
            elif getattr(picture_info, attr) is None:
                if something_changed is False:
                    logger.warning(
                        f"Photo #{existing_photo.id} '{picture_info.filename}' updates:"
                    )
                logger.warning(f"  - {f'{attr}:':<15} is NULL!")
                something_changed = True

        if something_changed:
            # existing_photo.filename = picture_info.filename
            # existing_photo.date_taken = picture_info.date_taken
            # existing_photo.user_id = picture_info.user_id
            # existing_photo.source_id = picture_info.source_id
            session.add(existing_photo)
            session.commit()
            return True, existing_photo.id
        else:
            return None, existing_photo.id

    # Insert new photo
    photo = Photo(
        filename=picture_info.filename,
        date_taken=picture_info.date_taken,
        album_id=album_id,
        user_id=picture_info.user_id,
        source_id=picture_info.source_id,
    )
    session.add(photo)
    session.commit()
    logger.info(f"Added photo: {picture_info.filename}")
    return False, photo.id


def insert_error(
    session: Session, error_message: str, album_id: Optional[int] = None
) -> None:
    """Insert an error."""
    error = Error(error_message=error_message, album_id=album_id)
    session.add(error)
    session.commit()
    logger.info(f"Error logged: {error_message}")


def link_user_to_album(session: Session, album_id: int, user_id: int) -> None:
    """Link a user to an album."""
    # Check if relationship already exists
    existing_link = (
        session.query(AlbumUser).filter_by(album_id=album_id, user_id=user_id).first()
    )

    if existing_link:
        logger.debug("User-album link already exists")
    else:
        link = AlbumUser(album_id=album_id, user_id=user_id)
        session.add(link)
        session.commit()
        logger.info("Linked user to album")


def album_exists(session: Session, album_title: str) -> bool:
    """Check if an album exists by title."""
    return (
        session.query(Album)
        .filter_by(source_title=album_title, source_type="gphoto")
        .first()
        is not None
    )


def get_album_photos_count(session: Session, album_id: int) -> int:
    """Get the number of photos for an album."""
    return session.query(Photo).filter_by(album_id=album_id).count()


def get_album_processed_items(session: Session, album_id: int) -> int:
    """Get the number of processed items for an album."""
    return session.query(Album).filter_by(id=album_id).first().processed_items


def update_album_processed_items(
    session: Session, album_id: int, processed_items: int
) -> None:
    """Update the number of processed items for an album."""
    logger.debug(f"Updating album {album_id} processed items to {processed_items}")
    album = session.query(Album).filter_by(id=album_id).first()
    if album:
        album.processed_items = processed_items
        session.commit()


def is_album_fully_processed(session: Session, album_id: int) -> bool:
    """Check if an album is fully processed."""
    album = session.query(Album).filter_by(id=album_id).first()
    if album:
        return album.processed_items >= album.items
    return False


def get_albums_without_immich_id(session: Session) -> list[Album]:
    """Get all albums that don't have an immich_id set.

    Args:
        session: Database session

    Returns:
        List[Album]: List of Album objects without immich_id
    """
    return (
        session.query(Album)
        .filter(or_(Album.immich_id.is_(None), Album.immich_id == ""))
        .all()
    )


def get_photos_from_db(
    session: Session, album_id: int | None = None, has_immich_id: bool | None = None
) -> list[Photo]:
    """Get photos from the database with optional filtering.

    Args:
        session: Database session
        album_id: Optional album ID to filter photos by
        has_immich_id: If True, only return photos with immich_id set.
                       If False, only return photos without immich_id.
                       If None, return all photos (no filtering by immich_id).

    Returns:
        List[Photo]: List of Photo objects matching the criteria
    """
    query = session.query(Photo)

    if album_id is not None:
        query = query.filter(Photo.album_id == album_id)

    if has_immich_id is not None:
        if has_immich_id:
            query = query.filter(Photo.immich_id.is_not(None))
        else:
            query = query.filter(Photo.immich_id.is_(None))

    return query.all()


def get_users(session: Session) -> list[User]:
    """Get all users from database.

    Returns:
        List of User objects
    """
    return session.query(User).all()


def get_albums_from_db(
    session: Session,
    limit: int | None = None,
    offset: int = 0,
    not_finished: bool = False,
    album_ids: list[int] | None = None,
) -> list[AlbumInfo]:
    """Get albums from database with pagination.

    Args:
        session: Database session
        limit: Maximum number of albums to return
        offset: Number of albums to skip
        not_finished: If True, only return albums that are not fully processed
    """
    query = session.query(
        Album.id,
        Album.source_url,
        Album.source_title,
        Album.items,
        Album.processed_items,
        Album.shared,
        Album.created_at,
    ).filter_by(source_type="gphoto")

    if not_finished:
        query = query.filter(Album.processed_items < Album.items)

    query = query.order_by(Album.id)

    if limit:
        query = query.offset(offset).limit(limit)

    if album_ids:
        query = query.filter(Album.id.in_(album_ids))

    res = query.all()
    return [
        AlbumInfo(
            album_id=album.id,
            title=album.source_title,
            items=album.items,
            shared=album.shared,
            processed_items=getattr(album, "processed_items", 0),
            created_at=getattr(album, "created_at", None),
            url=album.source_url,
        )
        for album in res
    ]


def get_users_from_db(session: Session) -> List[User]:
    """Get all users from database.

    Returns:
        List[User]: List of User objects with all fields including add_to_immich
    """
    return (
        session.query(User)
        .order_by(User.source_name)
        .filter_by(source_type="gphoto")
        .all()
    )


def get_database_stats(session: Session) -> Dict[str, Any]:
    """Get database statistics."""
    # Get album stats
    album_stats = (
        session.query(
            Album.id,
            Album.source_title,
            Album.source_type,
            Album.items,
            func.count(Photo.id).label("photo_count"),
            func.count(Error.id).label("error_count"),
        )
        .outerjoin(Photo, Album.id == Photo.album_id)
        .outerjoin(Error, Album.id == Error.album_id)
        .group_by(Album.id, Album.source_title, Album.source_type, Album.items)
        .all()
    )

    # Get user count
    user_count = session.query(User).count()

    # Get total photo count
    total_photos = session.query(Photo).count()

    # Get total error count
    total_errors = session.query(Error).count()

    return {
        "albums": album_stats,
        "total_albums": len(album_stats),
        "user_count": user_count,
        "total_users": user_count,
        "total_photos": total_photos,
        "total_errors": total_errors,
    }
