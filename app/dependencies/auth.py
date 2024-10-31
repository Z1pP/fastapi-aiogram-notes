from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas import UserEntity
from app.utils.utils import decode_jwt
from app.services import UserService, AuthService
from app.dependencies.user import get_user_service


security = HTTPBearer()


async def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    token = credentials.credentials
    try:
        payload = await decode_jwt(token)
        return payload
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    user_service: UserService = Depends(get_user_service),
) -> UserEntity:
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
) -> UserEntity:
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


async def get_auth_service(
    user_service: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(user_service)
