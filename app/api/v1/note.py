from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.exceptions.exceptions import NoteNotFoundException, UserNotFoundException
from app.schemas import NoteCreate, NoteResponse, NoteUpdate
from app.services import NoteService

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[NoteResponse])
async def get_notes(session: AsyncSession = Depends(get_async_session)):
    note_service = NoteService(session)
    return await note_service.get_notes()


@router.post("/create", response_model=NoteResponse, status_code=201)
async def create_note(
    note: NoteCreate, session: AsyncSession = Depends(get_async_session)
):
    note_service = NoteService(session)
    try:
        return await note_service.create_note(note)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{note_id}", status_code=204)
async def delete_note(note_id: int, session: AsyncSession = Depends(get_async_session)):
    note_service = NoteService(session)
    try:
        return await note_service.delete_note(note_id)
    except NoteNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int, note: NoteUpdate, session: AsyncSession = Depends(get_async_session)
):
    note_service = NoteService(session)
    try:
        return await note_service.update_note(note_id, note)
    except NoteNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/by_tags", response_model=list[NoteResponse])
async def get_notes_by_tags(
    tags: list[str], session: AsyncSession = Depends(get_async_session)
):
    note_service = NoteService(session)
    return await note_service.get_notes_by_tags(tags)
