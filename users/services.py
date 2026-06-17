from sqlalchemy.orm import Session

import users.storage as storage
from users.schemes import UserInDB, UserCreate, UserResponse

from typing import Optional

def is_admin(db: Session, user_id: int):
    user_record = storage.get_user_by_id(db, user_id)
    if user_record:
        user = UserInDB.model_validate(user_record)
        return user.is_admin
    return False


def get_user_by_id(db: Session, user_id: int) -> UserInDB| None:
    user_record = storage.get_user_by_id(db, user_id)
    if user_record is None:
        return None
    return UserInDB.model_validate(user_record)


def get_user_by_username(db: Session, username: str) -> UserInDB| None:
    user_record = storage.get_user_by_username(db, username)
    if user_record is None:
        return None
    return UserInDB.model_validate(user_record)


def create_user(db: Session, user_data: UserCreate) -> UserInDB:
    created = storage.create_user(db, user_data)
    return UserInDB.model_validate(created)

def update_password(db: Session, user_id: int, new_password) -> UserInDB | None:
    updated = storage.update_password(db, user_id, new_password)
    if updated is None:
        return None
    return UserInDB.model_validate(updated)


def delete_user(db: Session, user_id: int) -> bool:
    return storage.delete_user(db, user_id)


