from datetime import datetime
from pydantic import BaseModel, Field

from .tag_schema import TagResponse


class NoteBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=1)
    is_completed: bool = Field(default=False)
    tags: list[TagResponse] = Field(default_factory=list)


class NoteCreate(NoteBase):
    user_id: int


class NoteUpdate(NoteBase):
    pass


class NoteResponse(NoteBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

