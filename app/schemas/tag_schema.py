from datetime import datetime
from pydantic import BaseModel, Field


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagResponse(TagBase):
    pass
