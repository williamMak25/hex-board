from advanced_alchemy.base import UUIDv7AuditBase
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String,ForeignKey
from uuid import UUID
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.db.models import User


class Comment(UUIDv7AuditBase):
    __tablename__ = "comment"

    message: Mapped[str] = mapped_column(String(), server_default="", nullable=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user_account.id"), nullable=False)
    comment_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="comments",
        lazy="selectin",
        cascade="all, delete",
    )