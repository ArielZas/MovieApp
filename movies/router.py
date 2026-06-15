from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
import movies.services as services
from movies.schemes import MovieCreate, MovieResponse, MovieUpdate

# ============================================================
# movies/router.py  —  HTTP LAYER
#
# The only change from the in-memory version:
#   - Each handler now declares `db: Session = Depends(get_db)`
#   - `db` is passed through to the service layer
#
# FastAPI calls get_db(), gets the Session object, and injects
# it as `db` before the handler function runs. When the handler
# returns, FastAPI closes the session automatically (via the
# finally block in get_db()).
# ============================================================

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", response_model=list[MovieResponse])
def list_movies(db: Session = Depends(get_db)):
    return services.get_all_movies(db)


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = services.get_movie(db, movie_id)
    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with id {movie_id} not found",
        )
    return movie


@router.post("/", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(movie_data: MovieCreate, db: Session = Depends(get_db)):
    return services.create_movie(db, movie_data)


@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, movie_update: MovieUpdate, db: Session = Depends(get_db)):
    updated = services.update_movie(db, movie_id, movie_update)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with id {movie_id} not found",
        )
    return updated


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    deleted = services.delete_movie(db, movie_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with id {movie_id} not found",
        )


# ============================================================
# TODO EXERCISES — uncomment after implementing the matching
# service and storage functions.
# ============================================================

# TODO 1: GET /movies/genre/{genre}
# NOTE: Register this BEFORE /{movie_id} or FastAPI will try
# to parse "Action" as an integer movie ID and return 422.
#
# @router.get("/genre/{genre}", response_model=list[MovieResponse])
# def list_by_genre(genre: str, db: Session = Depends(get_db)):
#     return services.get_movies_by_genre(db, genre)


# TODO 2: GET /movies/search?q=inception
# Query params are plain function arguments with a default.
# `Query(min_length=1)` validates the ?q= value.
#
# from fastapi import Query
# @router.get("/search", response_model=list[MovieResponse])
# def search(q: str = Query(min_length=1), db: Session = Depends(get_db)):
#     return services.search_movies(db, q)


# TODO 3: GET /movies/top-rated?limit=5
#
# from fastapi import Query
# @router.get("/top-rated", response_model=list[MovieResponse])
# def top_rated(limit: int = Query(default=10, ge=1, le=100), db: Session = Depends(get_db)):
#     try:
#         return services.get_top_rated(db, limit)
#     except ValueError as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# TODO 4: GET /movies/year-range?start=2000&end=2010
#
# from fastapi import Query
# @router.get("/year-range", response_model=list[MovieResponse])
# def by_year_range(
#     start: int = Query(ge=1888),
#     end: int = Query(ge=1888),
#     db: Session = Depends(get_db),
# ):
#     try:
#         return services.get_movies_by_year_range(db, start, end)
#     except ValueError as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
