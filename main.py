from fastapi import FastAPI

from database import Base, engine

# Import all ORM models before calling create_all().
# SQLAlchemy discovers tables by scanning subclasses of Base —
# if a model module is never imported, its table won't be created.
import movies.models   # noqa: F401
import users.models    # noqa: F401
import watchlist.models  # noqa: F401

from movies.router import router as movies_router
from users.router import router as users_router
# from watchlist.router import router as watchlist_router

# ============================================================
# main.py  —  APPLICATION ENTRY POINT
#
# HOW TO RUN:
#   pip install -r requirements.txt
#   uvicorn main:app --reload
#
# Interactive docs:
#   http://127.0.0.1:8000/docs   ← Swagger UI (try everything here)
#   http://127.0.0.1:8000/redoc  ← clean read-only docs
#
# DATABASE:
#   A file called movieapp.db is created in this directory.
#   All data persists between server restarts.
#   To reset the DB, just delete movieapp.db and restart.
# ============================================================

# Create all tables that don't exist yet.
# This is safe to call on every startup — it uses CREATE TABLE IF NOT EXISTS.
# For production migrations (adding/altering columns), use Alembic instead.
Base.metadata.create_all(bind=engine)

# create the app
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
