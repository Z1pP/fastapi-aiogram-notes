from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, String, Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base
from .note_tag import NoteTag


if TYPE_CHECKING:
    from .tag import Tag
    from .user import User


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, name='id', index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), name='user_id')
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="notes", lazy="selectin")
    tags: Mapped[list["Tag"]] = relationship(
        secondary=NoteTag.__table__, 
        back_populates="notes", 
        lazy="selectin"
    )

