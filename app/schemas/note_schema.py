from datetime import datetime
from pydantic import BaseModel, Field

from .tag_schema import TagResponse


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
    created_at: datetime
    updated_at: datetime
    tags: list[TagResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True

