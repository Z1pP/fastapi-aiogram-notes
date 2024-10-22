from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.repositories import (
    SQLAlchemyUserRepository,
    SQLAlchemyNoteRepository,
    SQLAlchemyTagRepository,
)
from app.schemas import UserEntity
from app.services import (
    UserService,
    NoteService,
    TgProfileService,
    AuthService,
    TagService,
)
from app.usecases.note import (
    CreateNoteForUserUseCase,
    GetUserNotesUseCase,
    DeleteNoteForUserUseCase,
    UpdateNoteForUserUseCase,
    GetNotesByTagsUseCase,
)
from app.utils.utils import decode_jwt


security = HTTPBearer()


async def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    token = credentials.credentials
    try:
        payload = await decode_jwt(token)
        return payload
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_user_service(
    session: AsyncSession = Depends(get_async_session),
) -> UserService:
    user_repository = SQLAlchemyUserRepository(session)
    return UserService(user_repository)


async def get_note_service(
    session: AsyncSession = Depends(get_async_session),
) -> NoteService:
    note_repository = SQLAlchemyNoteRepository(session)
    return NoteService(note_repository)


async def get_tg_profile_service(
    session: AsyncSession = Depends(get_async_session),
) -> TgProfileService:
    return TgProfileService(session)


async def get_tag_service(
    session: AsyncSession = Depends(get_async_session),
) -> TagService:
    tag_repository = SQLAlchemyTagRepository(session)
    return TagService(tag_repository=tag_repository)


async def get_auth_service(
    user_service: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(user_service)


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


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    user_service: UserService = Depends(get_user_service),
) -> UserEntity:
    token_type = payload["type"]
    if token_type != "access":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type 'refresh' expected 'access'",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload["sub"]
    user = await user_service.get_user_by_id(user_id)
    return user


async def get_current_auth_user_refresh(
    payload: dict = Depends(get_current_token_payload),
    user_service: UserService = Depends(get_user_service),
) -> UserEntity:
    token_type = payload["type"]
    if token_type != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type 'access' expected 'refresh'",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload["sub"]
    user = await user_service.get_user_by_id(user_id)
    return user
