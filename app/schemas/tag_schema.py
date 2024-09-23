from datetime import datetime
from pydantic import BaseModel, Field


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagResponse(TagBase):
    created_at: datetime = Field(default=None)
    updated_at: datetime = Field(default=None)
