import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from core.config import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def _is_legacy_sha256(senha_hash: str) -> bool:
    return len(senha_hash) == 64 and all(char in "0123456789abcdef" for char in senha_hash.lower())


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    if _is_legacy_sha256(senha_hash):
        legacy_hash = hashlib.sha256(senha_plana.encode()).hexdigest()
        return hmac.compare_digest(legacy_hash, senha_hash)

    try:
        return pwd_context.verify(senha_plana, senha_hash)
    except (UnknownHashError, ValueError):
        return False


def criar_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def decodificar_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
