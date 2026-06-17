from sqlalchemy.orm import Session

from users.auth import hash_password
from users.models import UserModel
from users.schemes import UserCreate


def get_user_by_username(db: Session, username: str) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def create_user(db: Session, user_create: UserCreate) -> UserModel | None:
    if get_user_by_username(db, user_create.username) is not None:
        return None

    new_user = UserModel(
        username=user_create.username,
        hashed_password=hash_password(user_create.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session) -> list[UserModel]:
    return db.query(UserModel).all()


def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        return False
    db.delete(user)
    db.commit()
    return True

def update_password(db: Session, user_id: int, new_password: str) -> UserModel | None:
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user: 
        return None
    
    new_hashed_password = hash_password(new_password)
    setattr(user, "hashed_password", new_hashed_password)
    db.commit()
    db.refresh(user)
    return user