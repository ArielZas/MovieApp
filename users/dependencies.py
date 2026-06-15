from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from users.auth import decode_access_token
from users.models import UserModel
import users.storage as storage

# ============================================================
# users/dependencies.py  —  FASTAPI DEPENDENCY INJECTION
#
# get_current_user() now takes TWO injected dependencies:
#   - `token`  via OAuth2PasswordBearer (reads Authorization header)
#   - `db`     via get_db() (provides a DB session)
#
# FastAPI resolves dependencies recursively, so a route that
# declares Depends(get_current_user) automatically gets both
# a token AND a db session wired up for it.
# ============================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserModel:
    """
    Validates a Bearer JWT and returns the authenticated UserModel.
    Raises 401 if the token is missing, expired, tampered with,
    or belongs to a user that no longer exists in the database.

    Usage in any protected route:
        @router.get("/protected")
        def protected(user: UserModel = Depends(get_current_user)):
            return {"hello": user.username}
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = decode_access_token(token)
    if token_data is None or token_data.username is None:
        raise credentials_exception

    user = storage.get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception

    return user


# ============================================================
# TODO EXERCISE
# ============================================================

def get_current_user_optional(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserModel | None:
    """
    TODO: Soft authentication — returns the user if a valid token
    is present, or None instead of raising 401.
    Useful for public endpoints that show extra data for logged-in users.

    Hint:
        try:
            return get_current_user(token, db)
        except HTTPException:
            return None
    """
    raise NotImplementedError("TODO: implement get_current_user_optional")
