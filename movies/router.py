from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Annotated, Optional
from sqlalchemy.orm import Session

from database import get_db
import movies.services as services
from movies.schemes import MovieCreate, MovieResponse, MovieUpdate, MovieQuery
from users.dependencies import get_current_user, get_current_user_admin

router = APIRouter(prefix="/movies", tags=["Movies"], dependencies=[Depends(get_current_user)])


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


@router.post("/", response_model=MovieResponse)
def get_movies_by_filter(
    movie_query: Annotated[MovieQuery, Query()], 
    limit: Annotated[int, Query(10)],
    db: Session = Depends(get_db)
):
    return services.get_movies_by_filter(**movie_query.model_dump(), limit=limit, db=db)


@router.post("/top_rated", response_model=MovieResponse)
def get_top_rated(limit: int = 10, db: Session = Depends(get_db)):
    return services.get_top_rated(limit=limit, db=db)


@router.post("/", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(
    movie_data: MovieCreate, 
    db: Session = Depends(get_db),
    admin = Depends(get_current_user_admin),
):
    return services.create_movie(db, movie_data)


@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int, 
    movie_update: MovieUpdate, 
    db: Session = Depends(get_db),
    admin = Depends(get_current_user_admin),
):
    updated = services.update_movie(db, movie_id, movie_update)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with id {movie_id} not found",
        )
    return updated


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
    movie_id: int, 
    db: Session = Depends(get_db),
    admin = Depends(get_current_user_admin)
):
    deleted = services.delete_movie(db, movie_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with id {movie_id} not found",
        )
