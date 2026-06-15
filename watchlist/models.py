from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
)

from database import Base

# ============================================================
# watchlist/models.py  —  SQLALCHEMY ORM MODEL
#
# A watchlist item links one user to one movie.
# This is a classic "association table" — it represents a
# many-to-many relationship between users and movies, but with
# extra columns (watched, added_at) that store data ABOUT
# the relationship itself, not just the link.
#
# Relationships:
#   User  1 ──< WatchlistItem >── 1  Movie
#   (one user can have many items; one movie can be in many lists)
#
# The UniqueConstraint prevents the same movie appearing twice
# in one user's list.
# ============================================================


class WatchlistItem(Base):
    __tablename__ = "watchlist"

    # Enforce (user_id, movie_id) uniqueness at the database level.
    # Even if application code has a bug, the DB will reject duplicates.
    __table_args__ = (
        UniqueConstraint("user_id", "movie_id", name="uq_watchlist_user_movie"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # ForeignKey("users.id") tells SQLAlchemy this column references
    # the `id` column of the `users` table.
    # ondelete="CASCADE" means: if a User is deleted, all their
    # watchlist rows are automatically deleted too.
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    movie_id = Column(
        Integer,
        ForeignKey("movies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # default= runs in Python when a new row is created (not in SQL).
    # Using a lambda ensures the datetime is evaluated at insert time,
    # not when the module is first imported.
    added_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    watched = Column(Boolean, default=False, nullable=False)

    # nullable=True — only set once the user marks it as watched
    watched_at = Column(DateTime(timezone=True), nullable=True)
