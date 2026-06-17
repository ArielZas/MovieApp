from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from users.dependencies import get_current_user
from users.models import UserModel
from users.schemes import UserInDB
from watchlist.schemes import WatchlistItemCreate, WatchlistItemResponse, WatchlistItemUpdate
import watchlist.services as services

router = APIRouter(prefix="/watchlist", tags=["Watchlist"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[WatchlistItemResponse])
def list_watchlist(
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return services.get_watchlist(db, current_user.id)


@router.post("/", response_model=WatchlistItemResponse, status_code=status.HTTP_201_CREATED)
def add_to_watchlist(
    item_data: WatchlistItemCreate,
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    created = services.add_movie_to_watchlist(db, current_user.id, item_data)
    if created is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Movie is already in your watchlist",
        )
    return created


@router.put("/{movie_id}", response_model=WatchlistItemResponse)
def update_watchlist_item(
    movie_id: int,
    item_update: WatchlistItemUpdate,
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    updated = services.mark_watched(db, current_user.id, movie_id, item_update)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Watchlist entry not found")
    return updated


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_watchlist(
    movie_id: int,
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    removed = services.remove_movie_from_watchlist(db, current_user.id, movie_id)
    if not removed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Watchlist entry not found")


@router.get("/unwatched", response_model=list[WatchlistItemResponse])
def list_unwatched(
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return services.get_unwatched(db, current_user.id)
