from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException, ResponseValidationError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas import UserResponse, UserCreate
from app.services import UserService


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
async def get_users(session: AsyncSession = Depends(get_session)):
    user_service = UserService(session)
    return await user_service.get_users()


@router.post('/create', response_model=UserResponse)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user_seкvice = UserService(session)
    return await user_seкvice.create_user(user)