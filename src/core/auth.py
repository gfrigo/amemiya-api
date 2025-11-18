import time
from typing import Any, Dict
import bcrypt
from jose import jwt

from src.core.config import settings


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False


def create_access_token(subject: Dict[str, Any]) -> str:
    payload = {
        "sub": subject,
        "iat": int(time.time()),
        "exp": int(time.time()) + int(settings.ACCESS_TOKEN_EXPIRE_SECONDS or 3600)
    }
    token = jwt.encode(payload, settings.SECRET_KEY or "", algorithm=settings.JWT_ALGORITHM or "HS256")
    return token


def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT token, returning its payload or raising on error."""
    decoded = jwt.decode(token, settings.SECRET_KEY or "", algorithms=[settings.JWT_ALGORITHM or "HS256"])
    return decoded
