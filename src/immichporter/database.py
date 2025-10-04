"""Database operations for immichporter."""

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any, Optional
from rich.console import Console
from loguru import logger

from immichporter.models import Base, Album, User, Photo, Error, AlbumUser, SessionLocal

from immichporter.schemas import AlbumInfo

console = Console()


def get_db_session() -> Session:
    """Get a database session."""
    return SessionLocal()


def init_database(reset_db: bool = False) -> None:
    """Initialize the database."""
    if reset_db:
        Base.metadata.drop_all(bind=SessionLocal().bind)
    Base.metadata.create_all(bind=SessionLocal().bind)
    console.print("[green]Database initialized successfully[/green]")


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


def insert_or_update_user(session: Session, user_name: str) -> int:
    """Insert or update a user."""
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
        user = User(source_name=user_name, source_type="gphoto")
        session.add(user)
        session.commit()
        logger.info(f"Added user: {user_name}")
        return user.id


def insert_photo(
    session: Session, picture_info, user_id: int, album_id: int
) -> Optional[int]:
    """Insert a photo, returning the photo ID if successful, None if duplicate."""
    # Check if photo already exists
    existing_photo = (
        session.query(Photo)
        .filter_by(source_id=picture_info.source_id, album_id=album_id)
        .first()
    )

    if existing_photo:
        return None

    # Insert new photo
    photo = Photo(
        filename=picture_info.filename,
        date_taken=picture_info.date_taken,
        album_id=album_id,
        user_id=user_id,
        source_id=picture_info.source_id,
    )
    session.add(photo)
    session.commit()
    logger.info(f"Added photo: {picture_info.filename}")
    return photo.id


def insert_error(
    session: Session, error_message: str, album_id: Optional[int] = None
) -> None:
    """Insert an error."""
    error = Error(error_message=error_message, album_id=album_id)
    session.add(error)
    session.commit()
    console.print(f"[red]Error logged: {error_message}[/red]")


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


def update_album_processed_items(
    session: Session, album_id: int, processed_items: int
) -> None:
    """Update the number of processed items for an album."""
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


def get_albums_from_db(
    session: Session, limit: int = None, offset: int = 0
) -> list[AlbumInfo]:
    """Get albums from database with pagination."""
    query = (
        session.query(
            Album.id,
            Album.source_url,
            Album.source_title,
            Album.items,
            Album.shared,
        )
        .filter_by(source_type="gphoto")
        .order_by(Album.id)
    )

    if limit:
        query = query.offset(offset).limit(limit)

    res = query.all()
    return [
        AlbumInfo(
            album_id=album.id,
            title=album.source_title,
            items=album.items,
            shared=album.shared,
            url=album.source_url,
        )
        for album in res
    ]


def get_users_from_db(session: Session) -> List[User]:
    """Get all users from database."""
    return session.query(User).filter_by(source_type="gphoto").all()


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
