from pydantic import BaseModel
from typing import Optional


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    def to_entity(self) -> "TagEntity":
        return TagEntity(name=self.name)


class TagEntity(TagBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True

    def to_response(self) -> "TagResponse":
        return TagResponse(name=self.name)


class TagResponse(TagBase):
    pass

    class Config:
        from_attributes = True
