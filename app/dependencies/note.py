from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.services import NoteService, TagService
from app.repositories import SQLAlchemyNoteRepository
from app.usecases.note import (
    CreateNoteForUserUseCase,
    DeleteNoteForUserUseCase,
    GetNotesByTagsUseCase,
    GetUserNotesUseCase,
    UpdateNoteForUserUseCase,
)
from app.dependencies.tag import get_tag_service


async def get_note_service(
    session: AsyncSession = Depends(get_async_session),
) -> NoteService:
    note_repository = SQLAlchemyNoteRepository(session)
    return NoteService(note_repository)


async def get_user_notes_use_case(
    note_service: NoteService = Depends(get_note_service),
) -> GetUserNotesUseCase:
    return GetUserNotesUseCase(note_service=note_service)


async def update_note_for_user_use_case(
    note_service: NoteService = Depends(get_note_service),
    tag_service: TagService = Depends(get_tag_service),
) -> UpdateNoteForUserUseCase:
    return UpdateNoteForUserUseCase(note_service=note_service, tag_service=tag_service)


async def delete_note_for_user_use_case(
    note_service: NoteService = Depends(get_note_service),
) -> DeleteNoteForUserUseCase:
    return DeleteNoteForUserUseCase(note_service=note_service)


async def create_note_for_user_use_case(
    note_service: NoteService = Depends(get_note_service),
    tag_service: TagService = Depends(get_tag_service),
) -> CreateNoteForUserUseCase:
    return CreateNoteForUserUseCase(note_service=note_service, tag_service=tag_service)


async def get_notes_by_tags_use_case(
    note_service: NoteService = Depends(get_note_service),
    tag_service: TagService = Depends(get_tag_service),
) -> GetNotesByTagsUseCase:
    return GetNotesByTagsUseCase(note_service=note_service, tag_service=tag_service)
