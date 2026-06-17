from sqlalchemy import Column, Integer, String, Boolean

from database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    is_admin = Column(Boolean, default=False, nullable=False)
