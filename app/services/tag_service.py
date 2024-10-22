from app.models import Tag
from app.repositories.interfaces import ITagRepository
from app.exceptions import TagNotFoundException


class TagService:
    def __init__(self, tag_repository: ITagRepository):
        self.tag_repository = tag_repository

    async def _normalize_tag_name(self, tag_name: str) -> str:
        return tag_name.strip().lower().capitalize()

    async def get_or_create(self, tag_name: str) -> Tag:
        tag_name = await self._normalize_tag_name(tag_name=tag_name)
        tag_db = await self.tag_repository.get_by_name(name=tag_name)

        if tag_db is not None:
            return tag_db

        new_tag = Tag(name=tag_name)
        created_tag = await self.tag_repository.add(tag=new_tag)

        return created_tag

    async def delete_tag(self, tag_name: str) -> None:
        tag_db = await self.tag_repository.get_by_name(name=tag_name)
        if tag_db is not None:
            return await self.tag_repository.delete(tag=tag_db)
        raise TagNotFoundException(name=tag_name)
