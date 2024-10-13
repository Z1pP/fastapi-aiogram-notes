from app.exceptions import UserAlreadyExistsException, UserNotFoundException
from app.models import User
from app.schemas import UserResponse, UserCreate, UserUpdate
from app.utils.password import hash_password
from app.repositories import IUserRepository


class UserService:
    def __init__(self, user_repository: IUserRepository) -> None:
        self.user_repository = user_repository

    async def user_is_exists(self, email: str) -> bool:
        user = await self.user_repository.get_by_email(email)
        if user:
            raise UserAlreadyExistsException(email=email)

    async def create_user(self, user: UserCreate) -> UserResponse:
        user_db = await self.user_repository.get_by_email(user.email)
        if user_db:
            raise UserAlreadyExistsException(user.email)

        hashed_password = hash_password(user.password)

        dto_user = User(
            **user.model_dump(exclude="password"), hashed_password=hashed_password
        )

        return UserResponse.model_validate(await self.user_repository.add(dto_user))

    async def get_users(self) -> list[UserResponse]:
        users = await self.user_repository.get_all()
        return [UserResponse.model_validate(user) for user in users]

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id=user_id)
        if user is None:
            raise UserNotFoundException()
        return UserResponse.model_validate(user)

    async def get_user_by_email(self, email: str) -> UserResponse:
        user = await self.user_repository.get_by_email(email=email)
        if user is None:
            raise UserNotFoundException()
        return UserResponse.model_validate(user)

    async def update_user_by_id(self, user_id: int, user: UserUpdate) -> UserResponse:
        db_user = await self.get_user_by_id(user_id)

        update_data = user.model_dump(exclude_unset=True)

        if "email" in update_data:
            existing_user = await self.user_repository.get_by_email(
                email=update_data["email"]
            )
            if existing_user and existing_user.id != user_id:
                raise UserAlreadyExistsException(update_data["email"])

        if "password" in update_data:
            update_data["hashed_password"] = hash_password(update_data.pop("password"))

        for key, value in update_data.items():
            setattr(db_user, key, value)

        return UserResponse.model_validate(await self.user_repository.update(db_user))

    async def delete_user_by_id(self, user_id: int) -> None:
        db_user = await self.get_user_by_id(user_id)

        await self.user_repository.delete(db_user)
