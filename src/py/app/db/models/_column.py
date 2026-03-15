from advanced_alchemy.base import UUIDv7AuditBase
from sqlalchemy.orm import Mapped ,mapped_column
from sqlalchemy import ForeignKey,String,Integer
from uuid import UUID
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models._card import Card

class Column(UUIDv7AuditBase):
    __tablename__ = "column"

    board_id: Mapped[UUID] = mapped_column(ForeignKey("board.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(200))
    col_position: Mapped[int] = mapped_column(Integer())
    cards: Mapped[list["Card"]] = relationship(
        back_populates="columns",
        lazy="selectin",
        cascade="all, delete",
        load_on_pending=True
    )
