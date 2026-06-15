from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import JWTError, jwt

from users.schemes import TokenData

# ============================================================
# users/auth.py  —  PASSWORD HASHING + JWT TOKENS
#
# HOW JWT (JSON Web Token) AUTHENTICATION WORKS:
#
#   1. User sends username + password to POST /users/login
#   2. We verify the password against the stored bcrypt hash
#   3. We create a signed JWT and return it to the client
#   4. Client stores the token and sends it on every request:
#        Authorization: Bearer eyJhbGciOi...
#   5. We decode + verify the token to identify the user
#      — no database lookup needed for authentication!
#
# The token is SIGNED (so it can't be forged), but NOT encrypted
# (the payload is base64, readable by anyone). Never put passwords
# or secrets inside a JWT payload.
#
# DEPENDENCIES:
#   pip install python-jose[cryptography] bcrypt
#
# NOTE: We call bcrypt directly rather than via passlib because
# passlib's bcrypt backend is incompatible with bcrypt >= 4.0.
# ============================================================

# Used to sign and verify JWT tokens.
# IN PRODUCTION: store this in an environment variable, never in code.
SECRET_KEY = "CHANGE_ME_IN_PRODUCTION_USE_AN_ENV_VAR"

# HS256 = HMAC-SHA256, a symmetric algorithm (same key signs + verifies).
# RS256 (asymmetric, public/private key pair) is an alternative for
# systems where multiple services need to verify tokens independently.
ALGORITHM = "HS256"

# How long a token stays valid after login. After expiry the client
# must log in again to get a fresh token.
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=30)


def hash_password(plain_password: str) -> str:
    """
    Hash a plain-text password with bcrypt.
    bcrypt.gensalt() generates a unique random salt each time,
    so even two identical passwords produce different hashes —
    defeating rainbow table and pre-computation attacks.
    We encode to bytes (bcrypt requirement) and decode back to str for storage.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check whether a plain-text password matches a stored bcrypt hash.
    Returns True if they match, False otherwise.
    Always use this — never compare hashes with == directly.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(data: dict, expires_delta: timedelta = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    """
    Create a signed JWT access token.

    `data` should be {"sub": username}  ("sub" = subject, a JWT standard claim).
    The resulting token is a compact string: header.payload.signature
    """
    to_encode = data.copy()  # Never mutate the caller's dict

    # Compute absolute expiry time and store it as the "exp" JWT claim.
    # The jose library validates "exp" automatically when decoding.
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode["exp"] = expire

    # Encode + sign the payload. The result looks like:
    # "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ..."
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> TokenData | None:
    """
    Decode and verify a JWT token.
    Returns a TokenData object if the token is valid and not expired.
    Returns None if the token is invalid, expired, or was tampered with.
    """
    try:
        # jwt.decode() checks BOTH the signature and the expiry time.
        # If either fails it raises JWTError — we catch it below.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # "sub" is the standard JWT claim we put the username in.
        username: Optional[str] = payload.get("sub") 
        if username is None:
            return None

        return TokenData(username=username)
    except JWTError:
        # Token is expired, has a bad signature, or is malformed.
        return None
