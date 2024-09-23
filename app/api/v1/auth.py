from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.schemas import UserCreate, UserResponse
from app.services import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


