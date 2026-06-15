from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

# ============================================================
# movies/schemes.py  —  PYDANTIC SCHEMAS (API shapes)
#
# These schemas define what data looks like at the API boundary.
# They are SEPARATE from the SQLAlchemy model in models.py:
#
#   MovieModel    (models.py)  → maps to the DB table
#   MovieCreate   (here)       → validated from the request body
#   MovieUpdate   (here)       → partial update from the request body
#   MovieResponse (here)       → serialized into the JSON response
#
# The key addition vs the in-memory version:
#   ConfigDict(from_attributes=True) on MovieResponse
#   → tells Pydantic it can read field values from object attributes
#     (i.e. a SQLAlchemy ORM object), not just from a plain dict.
#   → enables: MovieResponse.model_validate(some_movie_model_instance)
# ============================================================


class MovieGenre(str, Enum):
    # str + Enum → serializes to "Action" not "MovieGenre.ACTION"
    ACTION = "Action"
    ADVENTURE = "Adventure"
    ANIMATION = "Animation"
    BIOGRAPHY = "Biography"
    COMEDY = "Comedy"
    CRIME = "Crime"
    DOCUMENTARY = "Documentary"
    DRAMA = "Drama"
    FAMILY = "Family"
    FANTASY = "Fantasy"
    HISTORY = "History"
    HORROR = "Horror"
    MUSICAL = "Musical"
    MYSTERY = "Mystery"
    ROMANCE = "Romance"
    SCI_FI = "Sci-Fi"
    SPORT = "Sport"
    THRILLER = "Thriller"
    WAR = "War"
    WESTERN = "Western"


class MovieCreate(BaseModel):
    """Client sends this JSON body to POST /movies."""
    title: str = Field(min_length=1, max_length=200, examples=["The Shawshank Redemption"])
    year: int = Field(ge=1888, le=2100, examples=[1994])
    genre: MovieGenre
    duration: int = Field(ge=1, description="Duration in minutes", examples=[142])
    director: str = Field(min_length=1, max_length=100, examples=["Frank Darabont"])
    description: Optional[str] = Field(default=None, max_length=1000)
    rating: Optional[float] = Field(default=None, ge=0.0, le=10.0)


class MovieUpdate(BaseModel):
    """All fields Optional — client sends only what they want changed."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    year: Optional[int] = Field(default=None, ge=1888, le=2100)
    genre: Optional[MovieGenre] = None
    duration: Optional[int] = Field(default=None, ge=1)
    director: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    rating: Optional[float] = Field(default=None, ge=0.0, le=10.0)


class MovieResponse(BaseModel):
    """
    Shape of the JSON we send back to the client.
    from_attributes=True is required so Pydantic can build this
    from a SQLAlchemy MovieModel ORM object (reads .id, .title, etc.).
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    year: int
    genre: MovieGenre
    duration: int
    director: str
    description: Optional[str] = None
    rating: Optional[float] = None
