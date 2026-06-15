from sqlalchemy import Column, Float, Integer, String, Text

from database import Base

# ============================================================
# movies/models.py  —  SQLALCHEMY ORM MODEL
#
# This class maps directly to a table in the database.
# SQLAlchemy uses it to:
#   - Generate the CREATE TABLE SQL statement
#   - Build SELECT / INSERT / UPDATE / DELETE queries
#
# IMPORTANT: Don't confuse this with the Pydantic schemas in
# schemes.py. They serve different purposes:
#
#   MovieModel    → how data is STORED (SQLAlchemy / DB layer)
#   MovieCreate   → what the CLIENT SENDS (Pydantic / API layer)
#   MovieResponse → what we SEND BACK  (Pydantic / API layer)
#
# A movie goes through this journey:
#   1. Client sends JSON  → FastAPI validates into MovieCreate
#   2. Storage creates a  MovieModel, commits it to the DB
#   3. Service converts   MovieModel → MovieResponse
#   4. FastAPI serializes MovieResponse back to JSON for the client
# ============================================================


class MovieModel(Base):
    __tablename__ = "movies"

    # primary_key=True → this column is the table's PK
    # autoincrement=True → DB assigns the next ID automatically (like AUTO_INCREMENT)
    # index=True → creates a DB index for fast lookups by ID
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    title = Column(String(200), nullable=False)
    year = Column(Integer, nullable=False)

    # Genre is stored as a plain string ("Action", "Drama", …).
    # The MovieGenre enum in schemes.py enforces valid values at the
    # API boundary; the DB column just stores the string.
    genre = Column(String(50), nullable=False)

    duration = Column(Integer, nullable=False)    # minutes
    director = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)     # Text = unlimited-length string
    rating = Column(Float, nullable=True)         # None = no rating yet
