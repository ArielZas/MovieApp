from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

# ============================================================
# watchlist/schemes.py  —  PYDANTIC SCHEMAS
#
# Same pattern as movies/schemes.py and users/schemes.py.
# These are provided for you — your TODO work is in
# watchlist/storage.py, watchlist/services.py, and
# watchlist/router.py.
# ============================================================


class WatchlistItemCreate(BaseModel):
    """What the client sends to add a movie to their watchlist."""
    movie_id: int


class WatchlistItemUpdate(BaseModel):
    """
    What the client sends to update a watchlist entry.
    Typically used to mark a movie as watched/unwatched.
    """
    watched: Optional[bool] = None
    watched_at: Optional[datetime] = None


class WatchlistItemResponse(BaseModel):
    """
    What we return to the client.
    from_attributes=True lets Pydantic read values from a
    SQLAlchemy ORM object (WatchlistItem) instead of a dict.
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    movie_id: int
    added_at: datetime
    watched: bool
    watched_at: Optional[datetime] = None
