from uuid import UUID

from advanced_alchemy.base import UUIDv7AuditBase
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.db.models._user import User
from app.db.models._board_members import board_member
class Board(UUIDv7AuditBase):
    __tablename__ = "board"

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200))
    bg_color: Mapped[str] = mapped_column(String(10))

    members:Mapped[list[User]] = relationship(
        secondary=lambda:board_member,
        back_populates="boards",
        lazy="selectin",
        cascade="all, delete"
    )