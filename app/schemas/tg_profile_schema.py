from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TgProfileBase(BaseModel):
    tg_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class TgProfileCreate(TgProfileBase):
    user_id: int

class TgProfileUpdate(BaseModel):
    tg_id: Optional[int] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class TgProfile(TgProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True