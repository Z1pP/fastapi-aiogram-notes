from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models import Tag
from app.repositories.interfaces import ITagRepository


class SQLAlchemyTagRepository(ITagRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_name(self, name: str) -> Optional[Tag]:
        query = select(Tag).where(Tag.name == name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def add(self, tag: Tag) -> Tag:
        self.session.add(tag)
        await self.session.commit()
        await self.session.refresh(tag)
        return tag

    async def delete(self, tag: Tag) -> None:
        await self.session.delete(tag)
        await self.session.commit()
