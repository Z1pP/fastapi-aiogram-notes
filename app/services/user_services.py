from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserResponse, UserCreate


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def create_user(self, user: UserCreate) -> UserResponse:
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