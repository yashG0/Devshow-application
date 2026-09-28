from datetime import UTC, datetime, timedelta

import jwt
from argon2 import PasswordHasher

from app.core.config import settings

password_hasher = PasswordHasher()

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        password_hasher.verify(password_hash, password)
        return True
    except Exception:
        return False


def create_access_token(user_id: int) -> str:
    expire = datetime.now(UTC) + timedelta(days=7)

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=ALGORITHM,
    )
