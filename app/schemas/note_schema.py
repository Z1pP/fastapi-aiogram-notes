from datetime import datetime
from pydantic import BaseModel, Field

from .tag_schema import TagResponse, TagCreate


class NoteBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=1)
    is_completed: bool = Field(default=False)
    


class NoteCreate(NoteBase):
    user_id: int
    tags: list[TagCreate]


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=5, max_length=100)
    description: str | None = Field(default=None, min_length=1)
    is_completed: bool | None = Field(default=None)
    tags: list[TagCreate] = Field(default=None)


class NoteResponse(NoteBase):
    id: int
    user_id: int
    tags: list[TagResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

