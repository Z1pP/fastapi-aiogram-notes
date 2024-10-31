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


class CreateUserUseCase:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service
        # self.validator_service = validator_service

    async def execute(self, user: UserEntity) -> UserResponse:
        # TODO: add validators to validate user data
        # self.validator_service.validate(user)

        user_db = await self.user_service.create_user(user=user)
        return user_db.to_response()


class UpdateUserDataUseCase:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service
        # self.validator_service = validator_service

    async def execute(self, user_id: int, user: UserEntity) -> UserResponse:
        # TODO: add validators to validate user data
        # self.validator_service.validate(user)

        user_db = await self.user_service.update_user_by_id(user_id=user_id, user=user)
        return user_db.to_response()


class DeleteUserUseCase:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    async def execute(self, user_id: int) -> None:
        await self.user_service.delete_user_by_id(user_id=user_id)
