from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.services.user_services import UserService
from app.repositories import SQLAlchemyUserRepository
from app.usecases.user import (
    GetAllUsersUseCase,
    GetUserByIdUseCase,
    UpdateUserDataUseCase,
    CreateUserUseCase,
    DeleteUserUseCase,
)


async def get_user_service(
    session: AsyncSession = Depends(get_async_session),
) -> UserService:
    user_repository = SQLAlchemyUserRepository(session=session)
    return UserService(user_repository=user_repository)


async def get_all_users_use_case(
    user_service: UserService = Depends(get_user_service),
) -> GetAllUsersUseCase:
    return GetAllUsersUseCase(user_service=user_service)


async def get_user_by_id_use_case(
    user_service: UserService = Depends(get_user_service),
) -> GetUserByIdUseCase:
    return GetUserByIdUseCase(user_service=user_service)


async def create_user_use_case(
    user_service: UserService = Depends(get_user_service),
) -> CreateUserUseCase:
    return CreateUserUseCase(user_service=user_service)


async def update_user_data_use_case(
    user_service: UserService = Depends(get_user_service),
) -> UpdateUserDataUseCase:
    return UpdateUserDataUseCase(user_service=user_service)


async def delete_user_use_case(
    user_service: UserService = Depends(get_user_service),
) -> DeleteUserUseCase:
    return DeleteUserUseCase(user_service=user_service)
