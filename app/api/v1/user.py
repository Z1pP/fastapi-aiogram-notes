from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.exceptions import BaseAppException
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.dependencies import (
    get_current_auth_user,
    get_all_users_use_case,
    get_user_by_id_use_case,
    create_user_use_case,
    update_user_data_use_case,
    delete_user_use_case,
)
from app.usecases.user import (
    GetAllUsersUseCase,
    GetUserByIdUseCase,
    CreateUserUseCase,
    UpdateUserDataUseCase,
    DeleteUserUseCase,
)


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(
    usecase: GetAllUsersUseCase = Depends(get_all_users_use_case),
):
    try:
        return await usecase.execute()
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate, usecase: CreateUserUseCase = Depends(create_user_use_case)
):
    try:
        return await usecase.execute(user=user.to_entity())
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: int, usecase: GetUserByIdUseCase = Depends(get_user_by_id_use_case)
):
    try:
        return await usecase.execute(user_id=user_id)
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.put("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    user_data: UserUpdate,
    user: UserResponse = Depends(get_current_auth_user),
    usecase: UpdateUserDataUseCase = Depends(update_user_data_use_case),
):
    try:
        return await usecase.execute(user_id=user.id, user=user_data.to_entity())
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: UserResponse = Depends(get_current_auth_user),
    usecase: DeleteUserUseCase = Depends(delete_user_use_case),
):
    try:
        await usecase.execute(user_id=user.id)
        return Response(status_code=204)
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
