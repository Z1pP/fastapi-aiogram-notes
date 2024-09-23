from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class NoteTag(Base):
    __tablename__ = "note_tags"

    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)
