from fastapi import FastAPI

from database import Base, engine

# Models must be imported before create_all so SQLAlchemy registers their tables.
import movies.models   # noqa: F401
import users.models    # noqa: F401
import watchlist.models  # noqa: F401

from movies.router import router as movies_router
from users.router import router as users_router
# from watchlist.router import router as watchlist_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie Library API",
    description=(
        "A RESTful API for managing a personal movie library. "
        "Supports user registration, JWT authentication, "
        "full CRUD for movies, and a personal watchlist."
    ),
    version="1.0.0",
)

app.include_router(movies_router)
app.include_router(users_router)
# app.include_router(watchlist_router)  ← uncomment when your watchlist is ready


@app.get("/", tags=["Health"])
def root():
    """Health check — confirms the server is running."""
    return {"status": "ok", "message": "Movie Library API is running"}
