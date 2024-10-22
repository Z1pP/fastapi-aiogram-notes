from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.models.base import Base
from app.models.note_tag import NoteTag
from app.schemas import NoteEntity


if TYPE_CHECKING:
    from .tag import Tag
    from .user import User


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, name="id", index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), name="user_id")
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="notes", lazy="selectin")
    tags: Mapped[list["Tag"]] = relationship(
        secondary=NoteTag.__table__, back_populates="notes", lazy="selectin"
    )

    def to_entity(self) -> "NoteEntity":
        return NoteEntity(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
            description=self.description,
            tags=self.tags,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
