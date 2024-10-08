from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.exceptions import UserNotFoundException, UserAlreadyExistsException
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.services import UserService
from app.dependencies import get_user_service, get_current_auth_user


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(
    user_service: UserService = Depends(get_user_service),
):
    try:
        return await user_service.get_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate, user_service: UserService = Depends(get_user_service)
):
    try:
        await user_service.create_user(user)
        return Response(status_code=201)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: int, user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.get_user_by_id(user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    user_updated: UserUpdate,
    user: UserResponse = Depends(get_current_auth_user),
    user_service: UserService = Depends(get_user_service),
):
    try:
        return await user_service.update_user(user.id, user_updated)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: UserResponse = Depends(get_current_auth_user),
    user_service: UserService = Depends(get_user_service),
):
    try:
        await user_service.delete_user(user.id)
        return Response(status_code=204)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
