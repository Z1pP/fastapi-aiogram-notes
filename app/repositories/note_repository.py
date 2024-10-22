from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Note, Tag
from app.repositories.interfaces import INoteRepository


class SQLAlchemyNoteRepository(INoteRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Note]:
        """
        Get all notes from the database.
        """
        query = select(Note).options(selectinload(Note.tags))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_user_id_and_tags(
        self, user_id: int, tags: List[str]
    ) -> List[Note]:
        """
        Get all notes by user ID and tags.
        """
        query = (
            select(Note)
            .join(Note.tags)
            .where(Tag.name.in_(tags), Note.user_id == user_id)
            .options(selectinload(Note.tags))
        )
        result = await self.session.execute(query)
        notes = result.scalars().unique().all()
        return notes

    async def get_by_id(self, note_id: int) -> Optional[Note]:
        """
        Get a note by its ID.
        """
        query = select(Note).where(Note.id == note_id).options(selectinload(Note.tags))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> List[Note]:
        """
        Get all notes by user ID.
        """
        query = (
            select(Note).where(Note.user_id == user_id).options(selectinload(Note.tags))
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_user_id_and_note_id(
        self, user_id: int, note_id: int
    ) -> Note | None:
        """
        Get a note by user ID and note ID.
        """
        query = (
            select(Note)
            .where(Note.id == note_id, Note.user_id == user_id)
            .options(selectinload(Note.tags))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def add(self, note: Note) -> Note:
        """
        Add a new note to the database.
        """
        self.session.add(note)
        await self.session.commit()
        await self.session.refresh(note)
        return note

    async def update(self, note: Note) -> Note:
        """
        Update a note in the database.
        """
        await self.session.commit()
        await self.session.refresh(note)
        return note

    async def delete(self, note: Note) -> None:
        """
        Delete a note from the database.
        """
        await self.session.delete(note)
        await self.session.commit()
