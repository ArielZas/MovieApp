from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50, examples=["john_doe"])
    password: str = Field(min_length=6, examples=["supersecret123"])


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class UserInDB(BaseModel):
    id: int
    username: str
    hashed_password: str
    is_admin: bool


class UserUpdate(BaseModel):
    username: str
    # new_username: Optional[str] = Field(min_length=3, max_length=50, examples=["john_doe"])
    password: str
    new_password: str = Field(min_length=6, examples=["supersecret123"])


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None
