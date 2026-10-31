from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import JWT_SECRET_KEY

ALGORITHM = "HS256"  # the signing method
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # a token stops working after 30 minutes

# Argon2id is a strong, modern password-hashing method
password_hash = PasswordHash.recommended()


def _get_secret() -> str:
    # Stop with a clear message if the key is missing from .env
    if not JWT_SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY is not configured")
    return JWT_SECRET_KEY


def hash_password(password: str) -> str:
    # Turn a password into a scrambled value that can't be reversed
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Check a typed password against the stored hash
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    # Build and sign a token that says who the user is and when it expires
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": str(user_id),  # "subject": the user's ID
        "exp": expires_at,  # expiration time
    }
    return jwt.encode(payload, _get_secret(), algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[int]:
    # Return the user's ID if the token is genuine and not expired, else None
    try:
        payload = jwt.decode(
            token,
            _get_secret(),
            algorithms=[ALGORITHM],
            options={"require": ["exp", "sub"]},
        )
        return int(payload["sub"])
    except (InvalidTokenError, ValueError, KeyError):
        return None