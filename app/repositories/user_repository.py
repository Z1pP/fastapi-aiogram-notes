from abc import ABC, abstractmethod
from typing import List, Optional
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import User
from app.db.database import get_async_session


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_all(self) -> List[User]:
        pass

    @abstractmethod
    async def add(self, user: User) -> User:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user: User) -> None:
        pass


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        query = (
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.notes), selectinload(User.tg_profile))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        query = (
            select(User)
            .where(User.email == email)
            .options(selectinload(User.notes), selectinload(User.tg_profile))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[User]:
        query = select(User).options(
            selectinload(User.notes), selectinload(User.tg_profile)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        return user

    async def update(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        return user

    async def delete(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()
