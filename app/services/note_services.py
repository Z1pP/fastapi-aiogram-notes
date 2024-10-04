from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.exceptions.exceptions import NoteNotFoundException
from app.schemas import NoteCreate, NoteResponse, NoteUpdate, TagCreate
from app.models import Tag, Note
from app.services import UserService


class NoteService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_service = UserService(self.session)

    async def _normalize_tags_name(self, tags: list[TagCreate]) -> list[TagCreate]:
        return [TagCreate(name=tag.name.lower().capitalize()) for tag in tags]

    async def _add_tags_to_note(self, tags: list[TagCreate]) -> list[Tag]:
        tags_list = list()
        tags = await self._normalize_tags_name(tags)

        for tag in tags:
            tag_db = await self.session.execute(select(Tag).where(Tag.name == tag.name))
            tag_db = tag_db.scalar_one_or_none()
            if not tag_db:
                tag_db = Tag(name=tag.name)
                self.session.add(tag_db)
            tags_list.append(tag_db)
        return tags_list

    async def create_note_for_user(
        self, user_id: int, note: NoteCreate
    ) -> NoteResponse:
        if note.tags:
            new_tags_db = await self._add_tags_to_note(note.tags)

        note_data = note.model_dump(exclude={"tags", "user_id"})
        note_db = Note(**note_data, tags=new_tags_db, user_id=user_id)
        self.session.add(note_db)

        await self.session.commit()
        await self.session.refresh(note_db)

        return note_db

    async def update_note_for_user(
        self, user_id: int, note_id: int, note: NoteUpdate
    ) -> NoteResponse:
        query = select(Note).where(Note.id == note_id, Note.user_id == user_id)
        result = await self.session.execute(query)
        db_note = result.scalar_one_or_none()

        if not db_note:
            raise NoteNotFoundException()

        note_data = note.model_dump(exclude={"tags"}, exclude_unset=True)
        for key, value in note_data.items():
            setattr(db_note, key, value)

        if note.tags:
            updated_tags_db = await self._add_tags_to_note(note.tags)
            db_note.tags = updated_tags_db

        await self.session.commit()
        await self.session.refresh(db_note)

        return db_note

    async def get_notes_for_user(self, user_id: int) -> list[NoteResponse] | None:
        query = (
            select(Note).where(Note.user_id == user_id).options(selectinload(Note.tags))
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_notes(self) -> list[NoteResponse]:
        query = select(Note).options(selectinload(Note.tags))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_notes_by_tags(self, tags: list[str]) -> list[NoteResponse]:
        query = (
            select(Note)
            .join(Note.tags)
            .where(Tag.name.in_(tags))
            .options(selectinload(Note.tags))
        )
        result = await self.session.execute(query)
        notes = result.scalars().unique().all()
        return notes

    async def delete_note_for_user(self, user_id: int, note_id: int) -> None:
        query = select(Note).where(Note.id == note_id, Note.user_id == user_id)
        result = await self.session.execute(query)
        note = result.scalar_one_or_none()
        if not note:
            raise NoteNotFoundException()
        await self.session.delete(note)
        await self.session.commit()
