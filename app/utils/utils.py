from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Literal
import jwt

from app.core.config import settings
from app.schemas import UserResponse


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


async def encode_jwt(
    payload: dict[str, Any],
    private_key_path: Path = settings.authjwt.private_key_path,
    algorithm: str = settings.authjwt.algorithm,
    expire_minutes: int = settings.authjwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    private_key = private_key_path.read_text()
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


async def decode_jwt(
    token: str | bytes,
    public_key_path: Path = settings.authjwt.public_key_path,
    algorithm: str = settings.authjwt.algorithm,
) -> dict[str, Any]:
    public_key = public_key_path.read_text()
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


async def create_token(
    token_type: Literal["access", "refresh"],
    token_data: dict[str, Any],
    expire_minutes: int = settings.authjwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return await encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


async def create_access_token(user: UserResponse) -> str:
    jwt_payload = {
        "sub": user.id,
        "email": user.email,
    }
    return await create_token(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
    )


async def create_refresh_token(user: UserResponse) -> str:
    jwt_payload = {
        "sub": user.id,
    }
    return await create_token(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(
            minutes=settings.authjwt.refresh_token_expire_minutes
        ),
    )
