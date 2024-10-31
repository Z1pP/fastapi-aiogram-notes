from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.services.user_services import UserService
from app.repositories import SQLAlchemyUserRepository


async def get_user_service(
    session: AsyncSession = Depends(get_async_session),
) -> UserService:
    user_repository = SQLAlchemyUserRepository(session)
    return UserService(user_repository)
