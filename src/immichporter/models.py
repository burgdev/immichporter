"""Shared database models for immichporter."""

from sqlalchemy import (
    create_engine,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    relationship,
    Mapped,
    mapped_column,
)

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_title: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    source_type: Mapped[str] = mapped_column(
        String, nullable=False
    )  # 'gphoto', 'local', etc.
    immich_title: Mapped[str | None] = mapped_column(
        String, unique=False, nullable=True
    )
    immich_id: Mapped[str | None] = mapped_column(
        String, nullable=True, unique=True, index=True
    )
    items: Mapped[int | None] = mapped_column(Integer)
    processed_items: Mapped[int] = mapped_column(Integer, default=0)
    shared: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    source_url: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # Relationships
    photos: Mapped[list["Photo"]] = relationship(
        "Photo", back_populates="album", cascade="all, delete-orphan"
    )
    errors: Mapped[list["Error"]] = relationship("Error", back_populates="album")
    users: Mapped[list["User"]] = relationship(
        "User", secondary="album_users", back_populates="albums"
    )

    def __repr__(self):
        return f"<Album(source_title='{self.source_title}', source_type='{self.source_type}', items={self.items}, shared={self.shared})>"


class User(Base):
    """SQLAlchemy model for users."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    source_type: Mapped[str] = mapped_column(
        String, nullable=False
    )  # 'gphoto', 'local', etc.
    immich_name: Mapped[str | None] = mapped_column(String, unique=False, nullable=True)
    immich_email: Mapped[str | None] = mapped_column(String, nullable=True)
    immich_user_id: Mapped[str | None] = mapped_column(String, nullable=True)
    immich_initial_password: Mapped[str | None] = mapped_column(String, nullable=True)
    add_to_immich: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    albums: Mapped[list["Album"]] = relationship(
        "Album", secondary="album_users", back_populates="users"
    )
    photos: Mapped[list["Photo"]] = relationship("Photo", back_populates="user")

    def __repr__(self):
        return f"<User(source_name='{self.source_name}', source_type='{self.source_type}', immich_name='{self.immich_name}', immich_email='{self.immich_email}')>"


class Photo(Base):
    """SQLAlchemy model for photos."""

    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    date_taken: Mapped[DateTime | None] = mapped_column(DateTime)
    album_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("albums.id", ondelete="CASCADE")
    )
    user_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL")
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    source_id: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, index=True
    )
    immich_id: Mapped[str | None] = mapped_column(
        String, nullable=True, unique=True, index=True
    )
    saved_to_your_photos: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    # Relationships
    album: Mapped[Album | None] = relationship("Album", back_populates="photos")
    user: Mapped[User | None] = relationship("User", back_populates="photos")

    def __repr__(self):
        return f"<Photo(filename='{self.filename}', date_taken={self.date_taken})>"


class Error(Base):
    """SQLAlchemy model for errors."""

    __tablename__ = "errors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    error_message: Mapped[str] = mapped_column(String, nullable=False)
    album_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("albums.id", ondelete="SET NULL")
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # Relationships
    album: Mapped[Album | None] = relationship("Album", back_populates="errors")

    def __repr__(self):
        return f"<Error(error_message='{self.error_message[:50]}...')>"


class AlbumUser(Base):
    """SQLAlchemy model for album-user relationships."""

    __tablename__ = "album_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    album_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("albums.id", ondelete="CASCADE")
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE")
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    __table_args__ = (
        UniqueConstraint("album_id", "user_id", name="unique_album_user"),
    )

    def __repr__(self):
        return f"<AlbumUser(album_id={self.album_id}, user_id={self.user_id})>"
