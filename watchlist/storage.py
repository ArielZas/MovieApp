from sqlalchemy.orm import Session

from watchlist.models import WatchlistItem
from watchlist.schemes import WatchlistItemCreate, WatchlistItemUpdate

# ============================================================
# watchlist/storage.py  —  DATA LAYER  (YOUR TODO)
#
# Implement each function below using the same SQLAlchemy
# patterns you've seen in movies/storage.py and users/storage.py.
#
# Quick reference:
#   db.query(WatchlistItem)                    → start a SELECT
#   .filter(WatchlistItem.user_id == user_id)  → WHERE clause
#   .filter(WatchlistItem.movie_id == movie_id)
#   .first()                                   → one row or None
#   .all()                                     → list of rows
#   db.add(obj) / db.commit() / db.refresh(obj)  → INSERT
#   setattr(obj, field, value) + db.commit()   → UPDATE
#   db.delete(obj) + db.commit()               → DELETE
# ============================================================


def get_watchlist_for_user(db: Session, user_id: int) -> list[WatchlistItem]:
    """
    TODO: Return all watchlist items belonging to the given user.

    SELECT * FROM watchlist WHERE user_id = :user_id
    """
    raise NotImplementedError("TODO: implement get_watchlist_for_user")


def get_watchlist_item(db: Session, user_id: int, movie_id: int) -> WatchlistItem | None:
    """
    TODO: Find a specific watchlist entry by user + movie combination.

    Chain two .filter() calls to match both columns.
    Returns None if the movie isn't in the user's watchlist.
    """
    raise NotImplementedError("TODO: implement get_watchlist_item")


def add_to_watchlist(db: Session, user_id: int, item_data: WatchlistItemCreate) -> WatchlistItem | None:
    """
    TODO: Add a movie to a user's watchlist.
    Return None if the movie is already in their watchlist
    (the UniqueConstraint in the model would reject it anyway —
    checking first gives a cleaner error to the caller).

    Steps:
      1. Call get_watchlist_item(db, user_id, item_data.movie_id)
      2. If it already exists, return None
      3. Otherwise create a WatchlistItem(user_id=user_id, movie_id=item_data.movie_id)
      4. db.add / db.commit / db.refresh, then return it
    """
    raise NotImplementedError("TODO: implement add_to_watchlist")


def update_watchlist_item(
    db: Session,
    user_id: int,
    movie_id: int,
    item_update: WatchlistItemUpdate,
) -> WatchlistItem | None:
    """
    TODO: Update a watchlist entry (e.g. mark as watched).
    Return None if the entry doesn't exist.

    Same setattr() loop pattern as update_movie() in movies/storage.py:
        update_data = item_update.model_dump(exclude_none=True)
        for field, value in update_data.items():
            setattr(item, field, value)
        db.commit()
        db.refresh(item)
    """
    raise NotImplementedError("TODO: implement update_watchlist_item")


def remove_from_watchlist(db: Session, user_id: int, movie_id: int) -> bool:
    """
    TODO: Remove a movie from a user's watchlist.
    Return True if deleted, False if it wasn't there.

    Same pattern as delete_movie() in movies/storage.py.
    """
    raise NotImplementedError("TODO: implement remove_from_watchlist")


def get_unwatched_for_user(db: Session, user_id: int) -> list[WatchlistItem]:
    """
    TODO: Return only the unwatched items in a user's watchlist.

    Filter on TWO columns:
        WatchlistItem.user_id == user_id
        WatchlistItem.watched == False
    """
    raise NotImplementedError("TODO: implement get_unwatched_for_user")
