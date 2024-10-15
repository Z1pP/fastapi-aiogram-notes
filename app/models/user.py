from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.schemas import UserEntity

from .base import Base

if TYPE_CHECKING:
    from .note import Note
    from .tg_profile import TgProfile


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    notes: Mapped[list["Note"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    tg_profile: Mapped["TgProfile"] = relationship(
        uselist=False,
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            email=self.email,
            hashed_password=self.hashed_password,
            created_at=self.created_at,
            updated_at=self.updated_at,
            notes=self.notes,
            tg_profile=self.tg_profile,
        )
