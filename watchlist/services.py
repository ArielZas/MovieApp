from sqlalchemy.orm import Session

import watchlist.storage as storage
from watchlist.schemes import WatchlistItemCreate, WatchlistItemResponse, WatchlistItemUpdate

# ============================================================
# watchlist/services.py  —  BUSINESS LOGIC LAYER  (YOUR TODO)
#
# After implementing watchlist/storage.py, come back here and
# implement each service function. The pattern is the same as
# movies/services.py:
#
#   1. Call the matching storage function with (db, ...)
#   2. Handle None returns (convert to the right response)
#   3. Convert ORM objects → Pydantic with model_validate()
#
# WatchlistItemResponse already has from_attributes=True.
# ============================================================


def get_watchlist(db: Session, user_id: int) -> list[WatchlistItemResponse]:
    """
    TODO: Fetch all watchlist items for a user and convert to response schema.
    One liner:
        return [WatchlistItemResponse.model_validate(i)
                for i in storage.get_watchlist_for_user(db, user_id)]
    """
    raise NotImplementedError("TODO: implement get_watchlist service")


def add_movie_to_watchlist(
    db: Session,
    user_id: int,
    item_data: WatchlistItemCreate,
) -> WatchlistItemResponse | None:
    """
    TODO: Add a movie to the watchlist.
    Return None if the movie is already there (caller returns 409).
    """
    raise NotImplementedError("TODO: implement add_movie_to_watchlist service")


def mark_watched(
    db: Session,
    user_id: int,
    movie_id: int,
    item_update: WatchlistItemUpdate,
) -> WatchlistItemResponse | None:
    """
    TODO: Update a watchlist entry (mark watched/unwatched).
    Return None if the entry doesn't exist (caller returns 404).
    """
    raise NotImplementedError("TODO: implement mark_watched service")


def remove_movie_from_watchlist(db: Session, user_id: int, movie_id: int) -> bool:
    """
    TODO: Remove a movie from the watchlist.
    Return True/False from storage directly.
    """
    raise NotImplementedError("TODO: implement remove_movie_from_watchlist service")


def get_unwatched(db: Session, user_id: int) -> list[WatchlistItemResponse]:
    """
    TODO: Return only unwatched items for a user.
    """
    raise NotImplementedError("TODO: implement get_unwatched service")
