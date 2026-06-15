from sqlalchemy.orm import Session

from movies.models import MovieModel
from movies.schemes import MovieCreate, MovieUpdate

# ============================================================
# movies/storage.py  —  DATA LAYER (now using SQLAlchemy)
#
# Every function here takes `db: Session` as its first argument.
# The Session object is created per-request by the get_db()
# dependency in database.py and passed down through:
#
#   Router (injects db via Depends) → Service → Storage
#
# KEY SQLALCHEMY PATTERNS USED HERE:
#
#   db.query(Model)               → start a SELECT query
#   .filter(Model.col == value)   → add a WHERE clause
#   .all()                        → fetch all matching rows (list)
#   .first()                      → fetch first row or None
#   db.add(obj)                   → stage an INSERT
#   db.commit()                   → write staged changes to disk
#   db.refresh(obj)               → reload obj from DB (gets generated id)
#   db.delete(obj)                → stage a DELETE
#   setattr(obj, field, value)    → modify an ORM object's column
# ============================================================


def get_all_movies(db: Session) -> list[MovieModel]:
    """SELECT * FROM movies"""
    return db.query(MovieModel).all()


def get_movie_by_id(db: Session, movie_id: int) -> MovieModel | None:
    """SELECT * FROM movies WHERE id = :movie_id LIMIT 1"""
    return db.query(MovieModel).filter(MovieModel.id == movie_id).first()


def create_movie(db: Session, movie_data: MovieCreate) -> MovieModel:
    """
    INSERT INTO movies (...) VALUES (...)
    model_dump() converts the Pydantic object to a dict so we can
    unpack it as keyword arguments into MovieModel().
    The genre field is a MovieGenre enum that inherits from str,
    so SQLAlchemy stores its string value ("Action", etc.) directly.
    """
    new_movie = MovieModel(**movie_data.model_dump())
    db.add(new_movie)
    db.commit()
    # refresh() re-reads the row from the DB so `new_movie.id` is
    # populated with the autoincrement value the DB assigned.
    db.refresh(new_movie)
    return new_movie


def update_movie(db: Session, movie_id: int, movie_update: MovieUpdate) -> MovieModel | None:
    """
    UPDATE movies SET ... WHERE id = :movie_id
    Only updates the fields the caller actually provided (not None).
    """
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if movie is None:
        return None

    # exclude_none=True gives us only the fields the client sent.
    update_data = movie_update.model_dump(exclude_none=True)

    # setattr() modifies each column on the ORM object.
    # SQLAlchemy tracks these changes and includes them in the next commit.
    for field, value in update_data.items():
        setattr(movie, field, value)

    db.commit()
    db.refresh(movie)
    return movie


def delete_movie(db: Session, movie_id: int) -> bool:
    """
    DELETE FROM movies WHERE id = :movie_id
    Returns True if a row was deleted, False if it didn't exist.
    """
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if movie is None:
        return False
    db.delete(movie)
    db.commit()
    return True


# ============================================================
# TODO EXERCISES
# Each function now also takes `db: Session` as its first arg.
# ============================================================

def get_movies_by_genre(db: Session, genre: str) -> list[MovieModel]:
    """
    TODO: SELECT * FROM movies WHERE genre = :genre

    SQLAlchemy filter syntax:
        db.query(MovieModel).filter(MovieModel.genre == genre).all()
    """
    raise NotImplementedError("TODO: implement get_movies_by_genre")


def get_movies_by_year_range(db: Session, start_year: int, end_year: int) -> list[MovieModel]:
    """
    TODO: SELECT * FROM movies WHERE year BETWEEN :start AND :end

    Chain two filters:
        .filter(MovieModel.year >= start_year)
        .filter(MovieModel.year <= end_year)
    Or combine with sqlalchemy.and_():
        from sqlalchemy import and_
        .filter(and_(MovieModel.year >= start_year, MovieModel.year <= end_year))
    """
    raise NotImplementedError("TODO: implement get_movies_by_year_range")


def search_movies_by_title(db: Session, query: str) -> list[MovieModel]:
    """
    TODO: SELECT * FROM movies WHERE title LIKE '%query%'

    SQLAlchemy LIKE (case-insensitive with ilike):
        .filter(MovieModel.title.ilike(f"%{query}%"))
    `ilike` is case-insensitive LIKE — supported by SQLite and PostgreSQL.
    """
    raise NotImplementedError("TODO: implement search_movies_by_title")


def get_top_rated_movies(db: Session, limit: int = 10) -> list[MovieModel]:
    """
    TODO: SELECT * FROM movies WHERE rating IS NOT NULL
          ORDER BY rating DESC LIMIT :limit

    Chain these calls:
        .filter(MovieModel.rating.isnot(None))
        .order_by(MovieModel.rating.desc())
        .limit(limit)
        .all()
    """
    raise NotImplementedError("TODO: implement get_top_rated_movies")


def get_movies_by_director(db: Session, director: str) -> list[MovieModel]:
    """
    TODO: Case-insensitive director search.
        .filter(MovieModel.director.ilike(f"%{director}%"))
    """
    raise NotImplementedError("TODO: implement get_movies_by_director")
