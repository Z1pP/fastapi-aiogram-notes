from fastapi import APIRouter, Depends, status

from app.schemas import UserCreate, UserResponse, TokenInfo
from app.services import AuthService
from app.dependencies import (
    get_auth_service,
    get_current_auth_user,
    get_current_auth_user_refresh,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login/", response_model=TokenInfo, status_code=status.HTTP_200_OK)
async def login(
    user: UserCreate, auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.login(user)


@router.post(
    "/refresh/",
    response_model=TokenInfo,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def refresh_token(
    user: UserResponse = Depends(get_current_auth_user_refresh),
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.refresh_token(user)


@router.get("/me/", response_model=UserResponse, status_code=200)
async def me(user: UserResponse = Depends(get_current_auth_user)):
    return user
