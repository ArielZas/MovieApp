from sqlalchemy import Column, Integer, String

from database import Base

# ============================================================
# users/models.py  —  SQLALCHEMY ORM MODEL
#
# Same pattern as movies/models.py — this class maps to the
# "users" table. See movies/models.py for a detailed explanation
# of the ORM model vs Pydantic schema distinction.
# ============================================================


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # unique=True → DB enforces no two users share a username
    # index=True  → fast lookups by username (used on every login)
    username = Column(String(50), unique=True, nullable=False, index=True)

    # We ONLY ever store the bcrypt hash, never the plain-text password.
    # String without a length limit → SQLAlchemy uses TEXT in SQLite,
    # which is fine since bcrypt hashes are always ~60 characters.
    hashed_password = Column(String, nullable=False)
