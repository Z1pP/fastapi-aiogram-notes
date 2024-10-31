from app.services import UserService
from app.schemas import UserResponse, UserEntity


class GetAllUsersUseCase:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    async def execute(self) -> list[UserResponse]:
        users = await self.user_service.get_users()
        return [user.to_response() for user in users]


class GetUserByIdUseCase:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    async def execute(self, user_id: int) -> UserResponse:
        user_db = await self.user_service.get_user_by_id(user_id=user_id)
        return user_db.to_response()
