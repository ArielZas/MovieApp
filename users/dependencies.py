from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from users.auth import decode_access_token
from users.models import UserModel
from users.schemes import UserInDB
import users.storage as storage
import users.services as services

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = decode_access_token(token)
    if token_data is None or token_data.username is None:
        raise credentials_exception

    user = services.get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception

    return user

def get_current_user_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = decode_access_token(token)
    if token_data is None or token_data.username is None:
        raise credentials_exception

    user = services.get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception

    if not user.is_admin:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="not admin"
        )

    return user


def get_current_user_optional(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserModel | None:
    raise NotImplementedError("TODO: implement get_current_user_optional")
