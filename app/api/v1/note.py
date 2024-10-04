from fastapi import APIRouter, Depends, HTTPException, status

from app.exceptions import *
from app.schemas import NoteCreate, NoteResponse, NoteUpdate, UserResponse
from app.services import NoteService
from app.dependencies import get_note_service, get_current_auth_user

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[NoteResponse])
async def get_notes(
    user: UserResponse = Depends(get_current_auth_user),
    note_service: NoteService = Depends(get_note_service),
):
    try:
        return await note_service.get_notes_for_user(user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    note: NoteCreate,
    user: UserResponse = Depends(get_current_auth_user),
    note_service: NoteService = Depends(get_note_service),
):
    try:
        return await note_service.create_note_for_user(user.id, note)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    user: UserResponse = Depends(get_current_auth_user),
    note_service: NoteService = Depends(get_note_service),
):
    try:
        return await note_service.delete_note_for_user(user.id, note_id)
    except NoteNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note: NoteUpdate,
    user: UserResponse = Depends(get_current_auth_user),
    note_service: NoteService = Depends(get_note_service),
):
    try:
        return await note_service.update_note_for_user(user.id, note_id, note)
    except NoteNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/by_tags", response_model=list[NoteResponse])
async def get_notes_by_tags(
    tags: list[str],
    user: UserResponse = Depends(get_current_auth_user),
    note_service: NoteService = Depends(get_note_service),
):
    return await note_service.get_notes_for_user_by_tags(user.id, tags)
