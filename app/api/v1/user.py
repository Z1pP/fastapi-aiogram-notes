from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_session
from app.schemas import UserResponse, UserCreate
from app.models import User as UserModel

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(UserModel).options(selectinload(UserModel.notes)))
    return result.scalars().all()


@router.post('/create', response_model=UserResponse)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    db_user = UserModel(**user)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        telegram_id=db_user.telegram_id or None,
        is_active=db_user.is_active,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
        notes=[]
    )
    