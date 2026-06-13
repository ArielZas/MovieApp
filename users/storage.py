from itertools import count
from passlib.hash import bcrypt

from users.schemes import UserCreate, UserInDB

users: dict[int, UserInDB] = {}
user_id_counter = count(0)

# ============================================================
# database.py
# Temporary user storage functions.
# Later these can be replaced with real SQL database logic.
# ============================================================

def get_user_by_username(username: str) -> UserInDB | None:
    for _, user in users.items():
        if user.username == username:
            return user
    return None   


def get_user_by_id(user_id: int) -> UserInDB | None:
    if user_id in users:
        return users[user_id]
    return None


def create_user(user_create: UserCreate) -> UserInDB | None:
    for id, user in users.items():
        if user.username == user_create.username:
            return None   

    new_user = UserInDB(
        username=user_create.username,
        id=next(user_id_counter),         
        hashed_password=bcrypt.hash(user_create.password)
    )

    users[new_user.id] = new_user
    return new_user
