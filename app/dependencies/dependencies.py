from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.schemas import UserResponse
from app.services import *
from app.utils.utils import decode_jwt


security = HTTPBearer()


async def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    token = credentials.credentials
    try:
        payload = await decode_jwt(token)
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_user_service(
    session: AsyncSession = Depends(get_async_session),
) -> UserService:
    return UserService(session)


async def get_note_service(
    session: AsyncSession = Depends(get_async_session),
) -> NoteService:
    return NoteService(session)


async def get_tg_profile_service(
    session: AsyncSession = Depends(get_async_session),
) -> TgProfileService:
    return TgProfileService(session)


async def get_auth_service(
    user_service: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(user_service)


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    token_type = payload["type"]
    if token_type != "access":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type 'refresh' expected 'access'",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload["sub"]
    user = await user_service.get_user_by_id(user_id)
    return user


async def get_current_auth_user_refresh(
    payload: dict = Depends(get_current_token_payload),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    token_type = payload["type"]
    if token_type != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type 'access' expected 'refresh'",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload["sub"]
    user = await user_service.get_user_by_id(user_id)
    return user
