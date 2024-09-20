from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.exceptions.exceptions import NoteNotFoundException, UserNotFoundException
from app.schemas import NoteCreate, NoteResponse, NoteUpdate
from app.models import Tag, Note
from .user_services import UserService


class NoteService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_service = UserService(self.session)
    
    async def _add_tags_to_note(self, note: list, tags: list[str]) -> None:
        for tag_name in tags:
            tag = await self.session.execute(select(Tag).where(Tag.name == tag_name))
            tag = tag.scalar_one_or_none()
            if not tag:
                tag = Tag(name=tag_name)
                self.session.add(tag)
            note.append(tag)
        return note

    async def create_note(self, note: NoteCreate) -> NoteResponse:
        # Проверка на существование пользователя
        await self.user_service._check_user_exist(note.user_id)
        
        tags_db = []
        if note.tags:
            tags_db = await self._add_tags_to_note(tags_db, note.tags)
        
        note_data = note.model_dump(exclude={'tags'})
        note_db = Note(**note_data, tags=tags_db)
        self.session.add(note_db)
        
        await self.session.commit()
        await self.session.refresh(note_db)

        return note_db
    
    async def update_note(self, note_id: int, note: NoteUpdate) -> NoteResponse:
        query = select(Note).where(Note.id == note_id)
        result = await self.session.execute(query)
        db_note = result.scalar_one_or_none()

        if not db_note:
            raise NoteNotFoundException()
        
        note_data = note.model_dump(exclude={'tags'}, exclude_unset=True)
        for key, value in note_data.items():
            setattr(db_note, key, value)
        
        tags_db = []
        if note.tags:
            tags_db = await self._add_tags_to_note(tags_db, note.tags)
            db_note.tags = tags_db
        
        await self.session.commit()
        await self.session.refresh(db_note)

        return db_note
                
    
    async def get_notes(self) -> list[NoteResponse]:
        result = await self.session.execute(select(Note).options(selectinload(Note.tags)))
        notes = result.scalars().all()
        return notes
    
    async def get_notes_by_tags(self, tags: list[str]) -> list[NoteResponse]:
        query = select(Note).join(Note.tags).where(Tag.name.in_(tags)).options(selectinload(Note.tags))
        result = await self.session.execute(query)
        notes = result.scalars().unique().all()
        return notes
    
    async def delete_note(self, note_id: int) -> None:
        query = select(Note).where(Note.id == note_id)
        result = await self.session.execute(query)
        note = result.scalar_one_or_none()
        if not note:
            raise NoteNotFoundException()
        await self.session.delete(note)
        await self.session.commit()