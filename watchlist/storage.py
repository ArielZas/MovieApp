from sqlalchemy.orm import Session

from watchlist.models import WatchlistItem
from watchlist.schemes import WatchlistItemCreate, WatchlistItemUpdate


def get_watchlist_for_user(db: Session, user_id: int) -> list[WatchlistItem]:
    return db.query(WatchlistItem).filter(WatchlistItem.user_id == user_id).all()

def get_watchlist_item(db: Session, user_id: int, movie_id: int) -> WatchlistItem | None:
    return db.query(WatchlistItem).filter(WatchlistItem.user_id == user_id and WatchlistItem.movie_id == movie_id).first()


def add_to_watchlist(db: Session, user_id: int, item_data: WatchlistItemCreate) -> WatchlistItem | None:
    if not get_watchlist_item(db, user_id, item_data.movie_id):
        return None
    
    watchlist_item = WatchlistItem(user_id=user_id, movie_id=item_data.movie_id)
    db.add(watchlist_item)
    db.commit()
    db.refresh(watchlist_item)
    return watchlist_item



def update_watchlist_item(
    db: Session,
    user_id: int,
    movie_id: int,
    item_update: WatchlistItemUpdate,
) -> WatchlistItem | None:
    watchedlist_item = get_watchlist_item(db, user_id, movie_id)

    if not watchedlist_item:
        return None

    update_data = item_update.model_dump(exclude_none=True)

    for field, value in update_data.items():
        setattr(watchedlist_item, field, value)
    
    db.commit()
    db.refresh(watchedlist_item)
    
    return watchedlist_item


def remove_from_watchlist(db: Session, user_id: int, movie_id: int) -> bool:
    watchlist_item = get_watchlist_item(db, user_id, movie_id)
    if not watchlist_item:
        return False

    db.delete(watchlist_item)
    db.commit()
    return True


def get_unwatched_for_user(db: Session, user_id: int) -> list[WatchlistItem]:
    return db.query(WatchlistItem).filter(WatchlistItem.watched == False).all()