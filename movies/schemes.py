from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class MovieGenre(str, Enum):
    # str mixin serializes to "Action" rather than "MovieGenre.ACTION"
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
    title: str = Field(min_length=1, max_length=200, examples=["The Shawshank Redemption"])
    year: int = Field(ge=1888, le=2100, examples=[1994])
    genre: MovieGenre
    duration: int = Field(ge=1, description="Duration in minutes", examples=[142])
    director: str = Field(min_length=1, max_length=100, examples=["Frank Darabont"])
    description: Optional[str] = Field(default=None, max_length=1000)
    rating: Optional[float] = Field(default=None, ge=0.0, le=10.0)


class MovieUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    year: Optional[int] = Field(default=None, ge=1888, le=2100)
    genre: Optional[MovieGenre] = None
    duration: Optional[int] = Field(default=None, ge=1)
    director: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    rating: Optional[float] = Field(default=None, ge=0.0, le=10.0)


class MovieResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    year: int
    genre: MovieGenre
    duration: int
    director: str
    description: Optional[str] = None
    rating: Optional[float] = None


class MovieQuery(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    start_year: Optional[int] = Field(default=None, ge=1888, le=2100)
    end_year: Optional[int] = Field(default=None, ge=1888, le=2100)
    genre: Optional[MovieGenre] = None
    duration: Optional[int] = Field(default=None, ge=1)
    director: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    rating: Optional[float] = Field(default=None, ge=0.0, le=100.0)

