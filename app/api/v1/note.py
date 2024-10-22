from fastapi import APIRouter, Depends, status, HTTPException

from app.exceptions import BaseAppException
from app.schemas import NoteCreate, NoteResponse, NoteUpdate, UserEntity
from app.dependencies import (
    get_current_auth_user,
    get_user_notes_use_case,
    create_note_for_user_use_case,
    delete_note_for_user_use_case,
    update_note_for_user_use_case,
    get_notes_by_tags_use_case,
)
from app.usecases.note import (
    CreateNoteForUserUseCase,
    GetUserNotesUseCase,
    DeleteNoteForUserUseCase,
    UpdateNoteForUserUseCase,
    GetNotesByTagsUseCase,
)

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[NoteResponse], status_code=status.HTTP_200_OK)
async def get_notes(
    user: UserEntity = Depends(get_current_auth_user),
    get_user_notes_use_case: GetUserNotesUseCase = Depends(get_user_notes_use_case),
):
    try:
        return await get_user_notes_use_case.execute(user_id=user.id)
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    note: NoteCreate,
    user: UserEntity = Depends(get_current_auth_user),
    create_note_for_user_use_case: CreateNoteForUserUseCase = Depends(
        create_note_for_user_use_case
    ),
):
    try:
        return await create_note_for_user_use_case.execute(
            user_id=user.id, note=note.to_entity()
        )
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    user: UserEntity = Depends(get_current_auth_user),
    delete_note_for_user_use_case: DeleteNoteForUserUseCase = Depends(
        delete_note_for_user_use_case
    ),
):
    try:
        return await delete_note_for_user_use_case.execute(
            user_id=user.id, note_id=note_id
        )
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note: NoteUpdate,
    user: UserEntity = Depends(get_current_auth_user),
    update_note_for_user_use_case: UpdateNoteForUserUseCase = Depends(
        update_note_for_user_use_case
    ),
):
    try:
        return await update_note_for_user_use_case.execute(
            user_id=user.id, note_id=note_id, note=note.to_entity()
        )
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("/by_tags", response_model=list[NoteResponse])
async def get_notes_by_tags(
    tags: list[str],
    user: UserEntity = Depends(get_current_auth_user),
    get_notes_by_tags_use_case: GetNotesByTagsUseCase = Depends(
        get_notes_by_tags_use_case
    ),
):
    return await get_notes_by_tags_use_case.execute(user_id=user.id, tags=tags)
