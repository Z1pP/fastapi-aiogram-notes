from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.exceptions.exceptions import UserAlreadyExistsException, UserNotFoundException
from app.schemas import UserCreate, UserResponse
from app.services import UserService


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
async def get_users(session: AsyncSession = Depends(get_async_session)):
    user_service = UserService(session)
    return await user_service.get_users()


@router.post('/create', response_model=UserResponse)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    user_seкvice = UserService(session)
    try:
        return await user_seкvice.create_user(user)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user_service = UserService(session)
    try:
        return await user_service.get_user_by_id(user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
