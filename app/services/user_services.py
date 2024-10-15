from app.exceptions import UserAlreadyExistsException, UserNotFoundException
from app.models import User
from app.schemas import UserEntity
from app.utils.password import hash_password
from app.repositories import IUserRepository


class UserService:
    def __init__(self, user_repository: IUserRepository) -> None:
        self.user_repository = user_repository

    async def user_is_exists(self, email: str) -> bool:
        """
        Check if user with email already exists
        """
        user = await self.user_repository.get_by_email(email=email)
        if user:
            raise UserAlreadyExistsException(email=email)

    async def create_user(self, user: UserEntity) -> UserEntity:
        """
        Create new user in database
        """
        user_db = await self.user_repository.get_by_email(email=user.email)
        if user_db:
            raise UserAlreadyExistsException(email=user.email)

        user.hashed_password = hash_password(user.password)

        new_user = User(**user.model_dump(exclude="password", exclude_unset=True))

        created_user = await self.user_repository.add(user=new_user)
        return created_user.to_entity()

    async def get_users(self) -> list[UserEntity]:
        """
        Get all users from database
        """
        users = await self.user_repository.get_all()
        return [user.to_entity() for user in users]

    async def get_user_by_id(self, user_id: int) -> UserEntity:
        """
        Get user by id from database
        """
        user = await self.user_repository.get_by_id(user_id=user_id)
        if user is None:
            raise UserNotFoundException()
        return user.to_entity()

    async def get_user_by_email(self, email: str) -> UserEntity:
        """
        Get user by email from database
        """
        user = await self.user_repository.get_by_email(email=email)
        if user is None:
            raise UserNotFoundException()
        return user.to_entity()

    async def update_user_by_id(self, user_id: int, user: UserEntity) -> UserEntity:
        """
        Update user by id from database
        """
        db_user = await self.user_repository.get_by_id(user_id)
        if db_user is None:
            raise UserNotFoundException()

        if user.email:
            # Check if email is already exists
            existing_user = await self.user_repository.get_by_email(email=user.email)
            if existing_user and (existing_user.id != db_user.id):
                raise UserAlreadyExistsException(email=user.email)

        if user.password:
            user.hashed_password = hash_password(user.password)

        updated_data = user.model_dump(exclude={"password"}, exclude_none=True)

        for key, value in updated_data.items():
            setattr(db_user, key, value)

        updated_user = await self.user_repository.update(user=db_user)
        return updated_user.to_entity()

    async def delete_user_by_id(self, user_id: int) -> None:
        """
        Delete user by id from database
        """
        db_user = await self.user_repository.get_by_id(user_id=user_id)
        if db_user is None:
            raise UserNotFoundException()

        await self.user_repository.delete(db_user)
