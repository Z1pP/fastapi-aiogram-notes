from typing import TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .note_tag import NoteTag


if TYPE_CHECKING:
    from .note import Note


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, name="id")
    name: Mapped[str] = mapped_column(String, nullable=False)

    notes: Mapped[list["Note"]] = relationship(
        secondary=NoteTag.__table__, back_populates="tags"
    )
