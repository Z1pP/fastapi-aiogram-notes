from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User

class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    token: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    token_type: Mapped[str] = mapped_column(String, nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False, 
        default=func.now()
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="token", lazy="selectin")