from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.services import TagService
from app.repositories import SQLAlchemyTagRepository


async def get_tag_service(
    session: AsyncSession = Depends(get_async_session),
) -> TagService:
    tag_repository = SQLAlchemyTagRepository(session)
    return TagService(tag_repository=tag_repository)
