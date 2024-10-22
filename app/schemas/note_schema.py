from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from .tag_schema import TagResponse, TagEntity


class NoteBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=1)


class NoteCreate(NoteBase):
    tags: list[str] | None = Field(default=None)

    def to_entity(self) -> "NoteEntity":
        return NoteEntity(
            title=self.title,
            description=self.description,
            tags=[TagEntity(name=tag) for tag in self.tags],
        )


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=5, max_length=100)
    description: str | None = Field(default=None, min_length=1)
    tags: list[str] | None = Field(default=None)

    def to_entity(self) -> "NoteEntity":
        return NoteEntity(
            title=self.title,
            description=self.description,
            tags=[TagEntity(name=tag) for tag in self.tags],
        )


class NoteResponse(NoteBase):
    id: int
    user_id: int
    tags: list[TagResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NoteEntity(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[TagEntity]] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    def to_response(self) -> "NoteResponse":
        return NoteResponse(**self.model_dump())
