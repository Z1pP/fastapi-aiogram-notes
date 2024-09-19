from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import UserAlreadyExistsException, UserNotFoundException
from app.models.user import User
from app.schemas.user_schema import UserResponse, UserCreate, UserUpdate
from app.utils.password import get_hashed_password


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def create_user(self, user: UserCreate) -> UserResponse:
        db_user = await self.get_user_by_email(user.email)
        if db_user:
            raise UserAlreadyExistsException(user.email)
        
        hashed_password = get_hashed_password(user.password)

        db_user = User(**user.model_dump(exclude="password"), hashed_password=hashed_password)
        self.session.add(db_user)

        await self.session.commit()
        await self.session.refresh(db_user)
        
        return db_user

    async def get_users(self) -> list[UserResponse]:
        query = select(User).options(
            selectinload(User.notes),
            selectinload(User.tg_profile)
        )
        result = await self.session.execute(query)
        users = result.scalars().all()
        return users
    
    async def get_user_by_id(self, user_id: int) -> UserResponse:
        query = select(User).where(User.id == user_id).options(
            selectinload(User.notes),
            selectinload(User.tg_profile)
        )
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise UserNotFoundException()
        return user
    
    async def get_user_by_email(self, email: str) -> UserResponse:
        query = select(User).where(User.email == email).options(
            selectinload(User.notes),
            selectinload(User.tg_profile)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def update_user(self, user_id: int, user: UserUpdate) -> UserResponse:
        db_user = await self.get_user_by_id(user_id)
        if db_user is None:
            raise UserNotFoundException()
        
        if user.password:
            hashed_password = get_hashed_password(user.password)

        if user.email:
            existing_user = await self.get_user_by_email(user.email)
            if existing_user:
                raise UserAlreadyExistsException(user.email)

        db_user = User(
            **user.model_dump(exclude="password"), 
            hashed_password=hashed_password
        )
        self.session.add(db_user)

        await self.session.commit()
        await self.session.refresh(db_user)
        
        return db_user
    
    async def delete_user(self, user_id: int) -> None:
        db_user = await self.get_user_by_id(user_id)
        if db_user is None:
            raise UserNotFoundException()
        
        await self.session.delete(db_user)
        await self.session.commit()
