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

    async def create_tg_profile(self, new_profile: TgProfileCreate) -> TgProfileResponse:
        
        tg_profile_db = TgProfile(**new_profile)
        self.session.add(tg_profile_db)
        self.session.commit()
        self.session.refresh(tg_profile_db)
        return tg_profile_db