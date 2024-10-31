from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.services import TgProfileService


async def get_tg_profile_service(
    session: AsyncSession = Depends(get_async_session),
) -> TgProfileService:
    return TgProfileService(session)
