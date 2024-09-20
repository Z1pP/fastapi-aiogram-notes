from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

from .note_schema import NoteResponse
from .tg_profile_schema import TgProfileResponse


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=8)


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    notes: list[NoteResponse] = Field(default_factory=list)
    tg_profile: Optional[TgProfileResponse] = None

    class Config:
        from_attributes = True
