from datetime import datetime
from pydantic import BaseModel, Field

from .tag import TagResponse


class NoteBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=1)
    is_completed: bool = Field(default=False)


class NoteCreate(NoteBase):
    user_id: int
    tags: list[str] = None


class NoteUpdate(NoteBase):
    tags: list[str] = None


class NoteResponse(NoteBase):
    id: int
    user_id: int
    create_at: datetime
    update_at: datetime
    tags: list[TagResponse]

    class Config:
        from_attributes = True

