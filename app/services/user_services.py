from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import UserAlreadyExistsException, UserNotFoundException
from app.models.user import User
from app.schemas.user import UserResponse, UserCreate, UserUpdate


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def create_user(self, user: UserCreate) -> UserResponse:
        db_user = await self.get_user_by_email(user)
        if db_user:
            raise UserAlreadyExistsException(user.email)
        
        hashed_password = user.password

        db_user = User(**user.model_dump(exclude="password"), hashed_password=hashed_password)
        self.session.add(db_user)

        await self.session.commit()
        await self.session.refresh(db_user)
        
        return UserResponse(
            id=db_user.id,
            username=db_user.username,
            is_active=db_user.is_active,
            email=db_user.email,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            notes=[]
        )

    async def get_users(self) -> list[UserResponse]:
        result = await self.session.execute(select(User).options(selectinload(User.notes)))
        users = result.scalars().all()
        return users
    
    async def get_user_by_id(self, user_id: int) -> UserResponse:
        result = await self.session.execute(select(User).where(User.id == user_id).options(selectinload(User.notes)))
        user = result.scalar_one_or_none()
        if user is None:
            raise UserNotFoundException()
        return user
    
    async def get_user_by_email(self, user: UserCreate) -> UserResponse:
        result = await self.session.execute(select(User).where(User.email == user.email))
        return result.scalar_one_or_none()
    
    async def update_user(self, user_id: int, user: UserUpdate) -> UserResponse:
        db_user = await self.get_user_by_id(user_id)
        if db_user is None:
            raise UserNotFoundException()
        
        if user.password:
            hashed_password = user.password
        else:
            hashed_password = db_user.hashed_password

        db_user = User(**user.model_dump(exclude="password"), hashed_password=hashed_password)
        self.session.add(db_user)

        await self.session.commit()
        await self.session.refresh(db_user)
        
        return UserResponse(
            id=db_user.id,
            username=db_user.username,
            is_active=db_user.is_active,
            email=db_user.email,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            notes=db_user.notes
        )
