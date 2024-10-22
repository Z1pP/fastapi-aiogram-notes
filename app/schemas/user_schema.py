from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    def to_entity(self) -> "UserEntity":
        return UserEntity(
            email=self.email,
            password=self.password,
        )


class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=8)

    def to_entity(self) -> "UserEntity":
        return UserEntity(
            email=self.email,
            password=self.password,
        )


class UserEntity(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    password: Optional[str] = None
    hashed_password: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    def to_response(self) -> "UserResponse":
        return UserResponse(
            id=self.id,
            email=self.email,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
