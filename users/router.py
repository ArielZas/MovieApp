from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from users.auth import create_access_token, verify_password
from users.dependencies import get_current_user, get_current_user_admin
from users.models import UserModel
from users.schemes import Token, UserCreate, UserResponse, UserInDB, UserUpdate

import users.storage as storage
import users.services as services

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    created = storage.create_user(db, user_data)
    if created is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken",
        )

    return created


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_record = storage.get_user_by_username(db, form_data.username)
    user = UserInDB.model_validate(user_record)

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
    return current_user



@router.delete("/", response_model=UserResponse)
def delete_user(
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if services.delete_user(db, current_user.id):
        return current_user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


# @router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
# def change_password(
#     request: ChangePasswordRequest,
#     current_user: UserModel = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     raise NotImplementedError("TODO")


@router.put("/", response_model=UserResponse)
def update_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    if not verify_password(UserUpdate.password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="wrong password"
        )
    
    user = services.update_password(db, current_user.id, user_update.new_password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user


@router.get("/",response_model=UserResponse)
def get_user(
    user_id: int,
    current_admin: UserInDB = Depends(get_current_user_admin),
    db: Session = Depends(get_db)
):
    user = services.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    return user



