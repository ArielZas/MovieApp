from sqlalchemy.orm import Session

import movies.storage as storage
from movies.schemes import MovieCreate, MovieResponse, MovieUpdate

from typing import Optional


def get_all_movies(db: Session) -> list[MovieResponse]:
    movies = storage.get_all_movies(db)
    return [MovieResponse.model_validate(m) for m in movies]

def get_movie(db: Session, movie_id: int) -> MovieResponse | None:
    movie = storage.get_movie_by_id(db, movie_id)
    if movie is None:
        return None
    return MovieResponse.model_validate(movie)


def create_movie(db: Session, movie_data: MovieCreate) -> MovieResponse:
    created = storage.create_movie(db, movie_data)
    return MovieResponse.model_validate(created)


def update_movie(db: Session, movie_id: int, movie_update: MovieUpdate) -> MovieResponse | None:
    updated = storage.update_movie(db, movie_id, movie_update)
    if updated is None:
        return None
    return MovieResponse.model_validate(updated)


def delete_movie(db: Session, movie_id: int) -> bool:
    return storage.delete_movie(db, movie_id)



def get_movies_by_genre(db: Session, genre: str) -> list[MovieResponse]:
    movies = storage.get_movies_by_genre(db, genre)
    return [MovieResponse.model_validate(m) for m in movies]

def search_movies(db: Session, title: str) -> list[MovieResponse]:
    movies = storage.search_movies_by_title(db, title)
    return [MovieResponse.model_validate(m) for m in movies]

def get_top_rated(db: Session, limit: int = 10) -> list[MovieResponse]:
    movies = storage.get_top_rated_movies(db, limit)
    return [MovieResponse.model_validate(m) for m in movies]

def get_movies_by_year_range(db: Session, start_year: int, end_year: int) -> list[MovieResponse]:
    movies = storage.get_movies_by_year_range(db, start_year, end_year)
    return [MovieResponse.model_validate(m) for m in movies]

def get_movies_by_filter(
        db: Session, 
        title: Optional[str], 
        start_year: Optional[int], 
        end_year: Optional[int], 
        genre: Optional[str], 
        director: Optional[str],
        rating: Optional[float],
        limit: Optional[int]
) -> list[MovieResponse]:
    movies = storage.get_movies_by_filter(
        db, 
        title, 
        start_year, 
        end_year, 
        genre, 
        director,
        rating, 
        limit
    )
    return [MovieResponse.model_validate(m) for m in movies]
