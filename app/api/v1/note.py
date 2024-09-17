from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.exceptions.exceptions import NoteNotFoundException, UserNotFoundException
from app.schemas import note as note_schema
from app.services import NoteService

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[note_schema.NoteResponse])
async def get_notes(session: AsyncSession=Depends(get_session)):
    note_service = NoteService(session)
    return await note_service.get_notes()


@router.post("/create", response_model=note_schema.NoteResponse, status_code=201)
async def create_note(note: note_schema.NoteCreate, session: AsyncSession=Depends(get_session)):
    note_service = NoteService(session)
    try:
        return await note_service.create_note(note)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{note_id}", status_code=204)
async def delete_note(note_id: int, session: AsyncSession=Depends(get_session)):
    note_service = NoteService(session)
    try:
        return await note_service.delete_note(note_id)
    except NoteNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/by_tags", response_model=list[note_schema.NoteResponse])
async def get_notes_by_tags(tags: list[str], session: AsyncSession=Depends(get_session)):
    note_service = NoteService(session)
    return await note_service.get_notes_by_tags(tags)