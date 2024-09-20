from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.exceptions.exceptions import *
from app.services import UserService
from app.schemas import TgProfileCreate, TgProfileResponse
from app.models import User, TgProfile

class TgProfileService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_servise = UserService(session)

    async def _check_tg_id_already_linked(self, tg_id: int) -> bool:
        query = select(TgProfile).where(TgProfile.tg_id == tg_id)
        result = await self.session.execute(query)
        tg_profile_db = result.scalar_one_or_none()
        if tg_profile_db:
            raise TgProfileAlreadyExistsException()

    async def create_tg_profile(self, new_profile: TgProfileCreate) -> TgProfileResponse:
        # Проверка на существование пользователя
        user = await self.user_servise.get_user_by_id(new_profile.user_id)
        if not user:
            raise UserNotFoundException()
        # Проверка на существование tg_id
        await self._check_tg_id_already_linked(new_profile.tg_id)

        tg_profile_db = TgProfile(**new_profile.model_dump())
        self.session.add(tg_profile_db)
        await self.session.commit()
        await self.session.refresh(tg_profile_db)
        return tg_profile_db