from sqlalchemy.orm import Session

from users.auth import hash_password
from users.models import UserModel
from users.schemes import UserCreate

# ============================================================
# users/storage.py  —  DATA LAYER (SQLAlchemy)
#
# Same patterns as movies/storage.py.
# All functions take `db: Session` as their first argument.
# ============================================================


def get_user_by_username(db: Session, username: str) -> UserModel | None:
    """
    SELECT * FROM users WHERE username = :username LIMIT 1
    Used during login and token validation.
    The `username` column has an index, so this is fast.
    """
    return db.query(UserModel).filter(UserModel.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> UserModel | None:
    """SELECT * FROM users WHERE id = :user_id LIMIT 1"""
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def create_user(db: Session, user_create: UserCreate) -> UserModel | None:
    """
    INSERT INTO users (username, hashed_password) VALUES (...)
    Returns None if the username is already taken.
    We check first instead of catching IntegrityError to keep
    the error handling clear and independent of the DB backend.
    """
    if get_user_by_username(db, user_create.username) is not None:
        return None  # Username taken — router will return 409

    new_user = UserModel(
        username=user_create.username,
        hashed_password=hash_password(user_create.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Populate new_user.id from the DB autoincrement
    return new_user


# ============================================================
# TODO EXERCISES
# ============================================================

def get_all_users(db: Session) -> list[UserModel]:
    """
    TODO: SELECT * FROM users
    One line — same pattern as get_all_movies() in movies/storage.py.
    """
    raise NotImplementedError("TODO: implement get_all_users")


def delete_user(db: Session, user_id: int) -> bool:
    """
    TODO: DELETE FROM users WHERE id = :user_id
    Return True if deleted, False if not found.
    Same pattern as delete_movie() in movies/storage.py.
    """
    raise NotImplementedError("TODO: implement delete_user")
