from sqlalchemy.orm import Session

import watchlist.storage as storage
from watchlist.schemes import WatchlistItemCreate, WatchlistItemResponse, WatchlistItemUpdate


def get_watchlist(db: Session, user_id: int) -> list[WatchlistItemResponse]:
    watchlist = storage.get_watchlist_for_user(db, user_id)
    return [WatchlistItemResponse.model_validate(w_item) for w_item in watchlist]


def add_movie_to_watchlist(
    db: Session,
    user_id: int,
    item_data: WatchlistItemCreate,
) -> WatchlistItemResponse | None:
    raise NotImplementedError("TODO: implement add_movie_to_watchlist service")


def mark_watched(
    db: Session,
    user_id: int,
    movie_id: int,
    item_update: WatchlistItemUpdate,
) -> WatchlistItemResponse | None:
    item = storage.update_watchlist_item(db, user_id, movie_id, item_update)
    if not item:
        return None
    return WatchlistItemResponse.model_validate(item)


def remove_movie_from_watchlist(db: Session, user_id: int, movie_id: int) -> bool:
    return storage.remove_from_watchlist(db, user_id, movie_id)


def get_unwatched(db: Session, user_id: int) -> list[WatchlistItemResponse]:
    watchlist = storage.get_unwatched_for_user(db, user_id)
    return [WatchlistItemResponse.model_validate(w_item) for w_item in watchlist]
