from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exceptions import *
from app.services import UserService
from app.schemas import TgProfileCreate, TgProfileResponse, TgProfileUpdate
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
        
    async def get_all_tg_profiles(self) -> list[TgProfileResponse]:
        query = select(TgProfile)
        result = await self.session.execute(query)
        tg_profiles_db = result.scalars().all()
        return list(tg_profiles_db)

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
    
    async def get_tg_profile_by_tg_id(self, tg_id: int) -> TgProfileResponse:
        query = select(TgProfile).where(TgProfile.tg_id == tg_id)
        result = await self.session.execute(query)
        tg_profile_db = result.scalar_one_or_none()
        if not tg_profile_db:
            raise TgProfileNotFoundException()
        return tg_profile_db
    
    async def update_tg_profile(self, tg_id: int, update_data: TgProfileUpdate) -> TgProfileResponse:
        tg_profile_db = await self.get_tg_profile_by_tg_id(update_data.tg_id)
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(tg_profile_db, field, value)
        self.session.add(tg_profile_db)
        await self.session.commit()
        await self.session.refresh(tg_profile_db)
        return tg_profile_db
    
    async def delete_tg_profile(self, tg_id: int) -> None:
        tg_profile_db = await self.get_tg_profile_by_tg_id(tg_id)
        await self.session.delete(tg_profile_db)
        await self.session.commit()