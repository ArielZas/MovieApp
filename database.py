from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# ============================================================
# database.py  —  DATABASE ENGINE & SESSION SETUP
#
# This file is the foundation of the persistence layer.
# Everything in movies/models.py and users/models.py builds
# on top of the Base class defined here.
#
# HOW SQLALCHEMY SESSIONS WORK:
#
#   engine        = the connection to the database file/server
#   SessionLocal  = a factory that creates Session objects
#   Session       = a "unit of work" — tracks changes to ORM
#                   objects and flushes them to the DB on commit
#
# One session per HTTP request is the standard FastAPI pattern.
# The get_db() dependency below creates a session, hands it to
# the route, then closes it when the request finishes.
# ============================================================

# SQLite stores everything in a local file — great for development.
# To switch to PostgreSQL in production, just change this URL:
#   "postgresql://user:password@localhost:5432/movieapp"
# Nothing else in the codebase needs to change.
DATABASE_URL = "sqlite:///./movieapp.db"

# create_engine() sets up the connection pool.
# check_same_thread=False is SQLite-specific: FastAPI may handle
# a request across multiple threads, which SQLite normally forbids.
# PostgreSQL/MySQL don't need this argument.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# sessionmaker() returns a class (not an instance).
# Each call to SessionLocal() creates a fresh Session object.
#   autocommit=False  → we call db.commit() manually; changes don't
#                       auto-persist, giving us transaction control
#   autoflush=False   → SQLAlchemy doesn't auto-sync pending changes
#                       to the DB before every query
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """
    All SQLAlchemy ORM models must inherit from this class.
    When Base.metadata.create_all(engine) is called (in main.py),
    SQLAlchemy scans every subclass of Base and creates its table
    if it doesn't already exist.
    """
    pass


def get_db():
    """
    FastAPI dependency — provides one DB session per HTTP request.

    The `yield` turns this into a generator-based context manager:
      - Code before yield runs BEFORE the route handler
      - Code after yield (in finally) runs AFTER the response is sent,
        even if an exception was raised inside the route

    Usage in any router file:
        from sqlalchemy.orm import Session
        from fastapi import Depends
        from database import get_db

        @router.get("/")
        def my_route(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db       # Hand the session to the route handler
    finally:
        db.close()     # Always return the connection to the pool
