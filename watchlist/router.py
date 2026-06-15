from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from users.dependencies import get_current_user
from users.models import UserModel
from watchlist.schemes import WatchlistItemCreate, WatchlistItemResponse, WatchlistItemUpdate
import watchlist.services as services

# ============================================================
# watchlist/router.py  —  HTTP LAYER  (YOUR TODO)
#
# Planned endpoints (all require authentication):
#
#   GET    /watchlist            → list the user's watchlist
#   POST   /watchlist            → add a movie to the watchlist
#   PUT    /watchlist/{movie_id} → mark watched / update entry
#   DELETE /watchlist/{movie_id} → remove from watchlist
#   GET    /watchlist/unwatched  → list only unwatched items
#
# The user_id always comes from the JWT token (get_current_user),
# NOT from the URL. This prevents users from reading/editing each
# other's watchlists.
#
# INSTRUCTIONS:
#   1. Implement all the storage and service TODOs first.
#   2. Then uncomment the routes below one at a time and test
#      each in the Swagger UI at http://127.0.0.1:8000/docs.
#   3. Don't forget to add `app.include_router(watchlist_router)`
#      in main.py once you're ready to wire it up.
# ============================================================

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])


# TODO 1: GET /watchlist
# Return the current user's full watchlist.
#
# @router.get("/", response_model=list[WatchlistItemResponse])
# def list_watchlist(
#     current_user: UserModel = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     return services.get_watchlist(db, current_user.id)


# TODO 2: POST /watchlist
# Add a movie to the current user's watchlist.
# Return 409 if it's already there.
#
# @router.post("/", response_model=WatchlistItemResponse, status_code=status.HTTP_201_CREATED)
# def add_to_watchlist(
#     item_data: WatchlistItemCreate,
#     current_user: UserModel = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     created = services.add_movie_to_watchlist(db, current_user.id, item_data)
#     if created is None:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="Movie is already in your watchlist",
#         )
#     return created


# TODO 3: PUT /watchlist/{movie_id}
# Update a watchlist entry (e.g. mark as watched).
# Return 404 if the entry doesn't exist.
#
# @router.put("/{movie_id}", response_model=WatchlistItemResponse)
# def update_watchlist_item(
#     movie_id: int,
#     item_update: WatchlistItemUpdate,
#     current_user: UserModel = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     updated = services.mark_watched(db, current_user.id, movie_id, item_update)
#     if updated is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Watchlist entry not found")
#     return updated


# TODO 4: DELETE /watchlist/{movie_id}
# Remove a movie from the watchlist.
#
# @router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
# def remove_from_watchlist(
#     movie_id: int,
#     current_user: UserModel = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     removed = services.remove_movie_from_watchlist(db, current_user.id, movie_id)
#     if not removed:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Watchlist entry not found")


# TODO 5: GET /watchlist/unwatched
# Return only the items the user hasn't watched yet.
# NOTE: Register this BEFORE /{movie_id} to avoid URL conflicts.
#
# @router.get("/unwatched", response_model=list[WatchlistItemResponse])
# def list_unwatched(
#     current_user: UserModel = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     return services.get_unwatched(db, current_user.id)
