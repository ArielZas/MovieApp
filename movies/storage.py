from sqlalchemy.orm import Session

from movies.models import MovieModel
from movies.schemes import MovieCreate, MovieUpdate

from typing import Optional


def get_all_movies(db: Session) -> list[MovieModel]:
    return db.query(MovieModel).all()


def get_movie_by_id(db: Session, movie_id: int) -> MovieModel | None:
    return db.query(MovieModel).filter(MovieModel.id == movie_id).first()


def create_movie(db: Session, movie_data: MovieCreate) -> MovieModel:
    new_movie = MovieModel(**movie_data.model_dump())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie


def update_movie(db: Session, movie_id: int, movie_update: MovieUpdate) -> MovieModel | None:
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if movie is None:
        return None

    update_data = movie_update.model_dump(exclude_none=True)

    for field, value in update_data.items():
        setattr(movie, field, value)

    db.commit()
    db.refresh(movie)
    return movie


def delete_movie(db: Session, movie_id: int) -> bool:
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if movie is None:
        return False
    db.delete(movie)
    db.commit()
    return True



def get_movies_by_genre(db: Session, genre: str) -> list[MovieModel]:
    return db.query(MovieModel).filter(MovieModel.genre == genre).all()

def get_movies_by_year_range(db: Session, start_year: int, end_year: int) -> list[MovieModel]:
    return db.query(MovieModel).filter(MovieModel.year >= start_year and MovieModel.year <= end_year).all()

def search_movies_by_title(db: Session, title: str) -> list[MovieModel]:
    return db.query(MovieModel).filter(MovieModel.title == title).all()

def get_top_rated_movies(db: Session, limit: int = 10) -> list[MovieModel]:
    return db.query(MovieModel).order_by(MovieModel.rating.desc()).limit(limit).all()

def get_movies_by_director(db: Session, director: str) -> list[MovieModel]:
    return db.query(MovieModel).filter(MovieModel.director == director).all()

def get_movies_by_filter(
    db: Session,
    title: Optional[str], 
    start_year: Optional[int],
    end_year: Optional[int],
    genre: Optional[str], 
    director: Optional[str],
    rating: Optional[float],
    limit: Optional[int],
) -> list[MovieModel]:
    filters = []

    if title is not None:
        filters.append(MovieModel.title == title)

    if start_year is not None:
        filters.append(MovieModel.year >= start_year)

    if end_year is not None:
        filters.append(MovieModel.year <= end_year)

    if genre is not None:
        filters.append(MovieModel.genre == genre)

    if director is not None:
        filters.append(MovieModel.director == director)

    if rating is not None:
        filters.append(MovieModel.rating == rating)

    query = db.query(MovieModel).filter(*filters)

    if limit is not None:
        query = query.limit(limit)

    return query.all()