from pydantic import BaseModel, ConfigDict, Field

# ============================================================
# users/schemes.py  —  PYDANTIC SCHEMAS (API shapes)
#
# Same pattern as movies/schemes.py.
# UserModel in users/models.py is the SQLAlchemy / DB layer.
# These schemas are the API layer — they define what comes in
# and goes out of the HTTP endpoints.
# ============================================================


class UserCreate(BaseModel):
    """Client sends this to POST /users/register."""
    username: str = Field(min_length=3, max_length=50, examples=["john_doe"])
    password: str = Field(min_length=6, examples=["supersecret123"])


class UserResponse(BaseModel):
    """
    Safe public shape — no password fields.
    from_attributes=True lets Pydantic read from a UserModel ORM object.
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class Token(BaseModel):
    """
    Returned after POST /users/login.
    Client stores this and attaches it to every protected request:
      Authorization: Bearer <access_token>
    """
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Decoded payload from inside a JWT token."""
    username: str | None = None
