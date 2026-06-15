from sqlalchemy.orm import Session

import movies.storage as storage
from movies.schemes import MovieCreate, MovieResponse, MovieUpdate

# ============================================================
# movies/services.py  —  BUSINESS LOGIC LAYER
#
# Services receive a db Session from the router and pass it
# to storage functions. They also convert SQLAlchemy ORM
# objects (MovieModel) into Pydantic schemas (MovieResponse)
# before returning to the router.
#
# MovieResponse has `from_attributes=True` in its ConfigDict,
# which is what allows model_validate() to read from an ORM object.
# ============================================================


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


# ============================================================
# TODO EXERCISES — implement after the matching storage TODOs
# ============================================================

def get_movies_by_genre(db: Session, genre: str) -> list[MovieResponse]:
    """
    TODO: Call storage.get_movies_by_genre(db, genre) and convert results.
    Same one-liner pattern as get_all_movies() above.
    """
    raise NotImplementedError("TODO: implement get_movies_by_genre service")


def search_movies(db: Session, query: str) -> list[MovieResponse]:
    """
    TODO: Call storage.search_movies_by_title(db, query) and convert.

    Extension: also search by director. Merge both result lists
    and deduplicate by id:
        title_results = storage.search_movies_by_title(db, query)
        dir_results   = storage.get_movies_by_director(db, query)
        seen = {m.id: m for m in title_results + dir_results}
        return [MovieResponse.model_validate(m) for m in seen.values()]
    """
    raise NotImplementedError("TODO: implement search_movies service")


def get_top_rated(db: Session, limit: int = 10) -> list[MovieResponse]:
    """
    TODO: Validate limit (1–100), then call storage.get_top_rated_movies().
    Raise ValueError for an out-of-range limit — the router catches it.
    """
    raise NotImplementedError("TODO: implement get_top_rated service")


def get_movies_by_year_range(db: Session, start_year: int, end_year: int) -> list[MovieResponse]:
    """
    TODO: Validate start_year <= end_year, then call storage.
    Raise ValueError if invalid — the router catches it.
    """
    raise NotImplementedError("TODO: implement get_movies_by_year_range service")
