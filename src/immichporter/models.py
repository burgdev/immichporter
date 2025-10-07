"""Shared database models for immichporter."""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Configuration
DATABASE_PATH = "immichporter.db"
BRAVE_EXECUTABLE = "/usr/bin/brave-browser"

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine(f"sqlite:///{DATABASE_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Album(Base):
    """SQLAlchemy model for albums."""

    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_title = Column(String, unique=False, nullable=False)
    source_type = Column(String, nullable=False)  # 'gphoto', 'local', etc.
    immich_title = Column(String, unique=False, nullable=True)
    immich_id = Column(String, nullable=True, unique=True, index=True)
    items = Column(Integer)
    processed_items = Column(Integer, default=0)
    shared = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    source_url = Column(String, unique=True, nullable=False)

    # Relationships
    photos = relationship("Photo", back_populates="album", cascade="all, delete-orphan")
    errors = relationship("Error", back_populates="album")
    users = relationship("User", secondary="album_users", back_populates="albums")

    def __repr__(self):
        return f"<Album(source_title='{self.source_title}', source_type='{self.source_type}', items={self.items}, shared={self.shared})>"


class User(Base):
    """SQLAlchemy model for users."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_name = Column(String, unique=False, nullable=False)
    source_type = Column(String, nullable=False)  # 'gphoto', 'local', etc.
    immich_name = Column(String, unique=False, nullable=True)
    immich_email = Column(String, nullable=True)
    immich_user_id = Column(Integer, nullable=True)
    immich_initial_password = Column(String, nullable=True)
    add_to_immich = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    albums = relationship("Album", secondary="album_users", back_populates="users")
    photos = relationship("Photo", back_populates="user")

    def __repr__(self):
        return f"<User(source_name='{self.source_name}', source_type='{self.source_type}', immich_name='{self.immich_name}', immich_email='{self.immich_email}')>"


class Photo(Base):
    """SQLAlchemy model for photos."""

    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    date_taken = Column(DateTime)
    album_id = Column(Integer, ForeignKey("albums.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime, default=func.now())
    filename = Column(String, nullable=False)
    source_id = Column(String, nullable=False, unique=True, index=True)
    immich_id = Column(String, nullable=True, unique=True, index=True)

    # Relationships
    album = relationship("Album", back_populates="photos")
    user = relationship("User", back_populates="photos")

    def __repr__(self):
        return f"<Photo(filename='{self.filename}', date_taken={self.date_taken})>"


class Error(Base):
    """SQLAlchemy model for errors."""

    __tablename__ = "errors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    error_message = Column(String, nullable=False)
    album_id = Column(Integer, ForeignKey("albums.id", ondelete="SET NULL"))
    created_at = Column(DateTime, default=func.now())

    # Relationships
    album = relationship("Album", back_populates="errors")

    def __repr__(self):
        return f"<Error(error_message='{self.error_message[:50]}...')>"


class AlbumUser(Base):
    """SQLAlchemy model for album-user relationships."""

    __tablename__ = "album_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    album_id = Column(Integer, ForeignKey("albums.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=func.now())
    __table_args__ = (
        UniqueConstraint("album_id", "user_id", name="unique_album_user"),
    )

    def __repr__(self):
        return f"<AlbumUser(album_id={self.album_id}, user_id={self.user_id})>"
