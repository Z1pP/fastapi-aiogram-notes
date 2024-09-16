from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_session
from app.models import Note as NoteModel, Tag as TagModel
from app.schemas import note as note_schema

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[note_schema.NoteResponse])
async def get_notes(session: AsyncSession=Depends(get_session)):
    result = await session.execute(select(NoteModel).options(selectinload(NoteModel.tags)))
    notes = result.scalars().all()
    return notes


@router.post("/create", response_model=note_schema.NoteResponse)
async def create_note(note: note_schema.NoteCreate, session: AsyncSession=Depends(get_session)):
    tags_db = []
    for tag_name in note.tags:
        tag = await session.execute(select(TagModel).where(TagModel.name == tag_name))
        tag = tag.scalar_one_or_none()
        if not tag:
            tag = TagModel(name=tag_name)
            session.add(tag)
        tags_db.append(tag)
    
    note_data = note.model_dump(exclude={'tags'})
    note_db = NoteModel(**note_data, tags=tags_db)
    session.add(note_db)
    
    await session.commit()
    await session.refresh(note_db)

    return note_db