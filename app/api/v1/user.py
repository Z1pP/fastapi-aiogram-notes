from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.exceptions import BaseAppException
from app.schemas import UserCreate, UserResponse, UserUpdate, UserEntity
from app.services import UserService
from app.dependencies import get_user_service, get_current_auth_user


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(
    user_service: UserService = Depends(get_user_service),
):
    try:
        users = await user_service.get_users()
        return [UserEntity.to_response(user) for user in users]
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate, user_service: UserService = Depends(get_user_service)
):
    try:
        created_user = await user_service.create_user(user=user.to_entity())
        return UserEntity.to_response(created_user)
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: int, user_service: UserService = Depends(get_user_service)
):
    try:
        user = await user_service.get_user_by_id(user_id)
        return UserEntity.to_response(user)
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.put("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    user_updated: UserUpdate,
    user: UserResponse = Depends(get_current_auth_user),
    user_service: UserService = Depends(get_user_service),
):
    try:
        return await user_service.update_user_by_id(
            user_id=user.id, user=user_updated.to_entity()
        )
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: UserResponse = Depends(get_current_auth_user),
    user_service: UserService = Depends(get_user_service),
):
    try:
        await user_service.delete_user_by_id(user.id)
        return Response(status_code=204)
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
