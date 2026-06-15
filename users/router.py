from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from users.auth import create_access_token, verify_password
from users.dependencies import get_current_user
from users.models import UserModel
from users.schemes import Token, UserCreate, UserResponse
import users.storage as storage

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    POST /users/register
    Creates a new account. Returns the user profile (no password).
    """
    created = storage.create_user(db, user_data)
    if created is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken",
        )
    # UserResponse has from_attributes=True, so we can return the
    # ORM object directly — FastAPI serializes it via response_model.
    return created


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    POST /users/login
    Exchange username + password for a JWT access token.
    Uses form data (OAuth2 standard), not JSON — the /docs UI supports this.
    """
    user = storage.get_user_by_username(db, form_data.username)

    # Same error for "user not found" and "wrong password" —
    # never reveal whether a particular username exists.
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
def get_me(current_user: UserModel = Depends(get_current_user)):
    """
    GET /users/me
    Returns the currently authenticated user's profile.
    get_current_user handles all token validation — if it returns,
    the user is authenticated. If not, FastAPI already sent a 401.
    """
    return current_user  # FastAPI serializes via UserResponse + from_attributes=True


# ============================================================
# TODO EXERCISES
# ============================================================

# TODO 1: GET /users/{user_id}  (public — no auth)
# Return a public user profile by ID. Raise 404 if not found.
#
# @router.get("/{user_id}", response_model=UserResponse)
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     user = storage.get_user_by_id(db, user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# TODO 2: POST /users/change-password  (protected)
# Add a ChangePasswordRequest schema to schemes.py with fields:
#   current_password: str
#   new_password: str = Field(min_length=6)
# Then:
#   1. verify_password(request.current_password, current_user.hashed_password)
#   2. setattr(current_user, "hashed_password", hash_password(request.new_password))
#   3. db.commit()
#
# @router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
# def change_password(
#     request: ChangePasswordRequest,
#     current_user: UserModel = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     raise NotImplementedError("TODO")
