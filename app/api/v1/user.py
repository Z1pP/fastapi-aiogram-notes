from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.exceptions import *
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.services import UserService


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
async def get_users(session: AsyncSession = Depends(get_async_session)):
    user_service = UserService(session)
    return await user_service.get_users()


@router.post("/create", response_model=UserResponse, status_code=201)
async def create_user(
    user: UserCreate, session: AsyncSession = Depends(get_async_session)
):
    user_seкvice = UserService(session)
    try:
        return await user_seкvice.create_user(user)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    user_service = UserService(session)
    try:
        return await user_service.get_user_by_id(user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, user: UserUpdate, session: AsyncSession = Depends(get_async_session)
):
    user_service = UserService(session)
    try:
        return await user_service.update_user(user_id, user)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user_service = UserService(session)
    try:
        await user_service.delete_user(user_id)
        return Response(status_code=204)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
