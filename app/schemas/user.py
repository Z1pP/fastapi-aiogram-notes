from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from .note import NoteResponse


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=100)
    telegram_id: Optional[int] = None
    is_active: bool = Field(default=True)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=8)


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    notes: list[NoteResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True
