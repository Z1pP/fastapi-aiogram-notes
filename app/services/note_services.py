from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.exceptions.exceptions import NoteNotFoundException, UserNotFoundException
from app.schemas.note import NoteCreate, NoteResponse
from app.models import Tag, Note
from .user_services import UserService


class NoteService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _check_user_exist(self, user_id: int) -> bool:
        user_service = UserService(self.session)
        user = await user_service.get_user_by_id(user_id)
        if user:
            return True
        return False

    async def create_note(self, note: NoteCreate) -> NoteResponse:
        if not await self._check_user_exist(note.user_id):
            raise UserNotFoundException()
        
        tags_db = []
        if note.tags:
            for tag_name in note.tags:
                tag = await self.session.execute(select(Tag).where(Tag.name == tag_name))
                tag = tag.scalar_one_or_none()
                if not tag:
                    tag = Tag(name=tag_name)
                    self.session.add(tag)
                tags_db.append(tag)
        
        note_data = note.model_dump(exclude={'tags'})
        note_db = Note(**note_data, tags=tags_db)
        self.session.add(note_db)
        
        await self.session.commit()
        await self.session.refresh(note_db)

        return note_db
    
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