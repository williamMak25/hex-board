from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy.base import UUIDv7AuditBase
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models._assignee import card_assignee
from app.lib.schema import PriorityEnum

if TYPE_CHECKING:
    from app.db.models._column import Column
    from app.db.models._user import User


class Card(UUIDv7AuditBase):
    __tablename__ = "card"

    col_id: Mapped[UUID] = mapped_column(ForeignKey("column.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    attachements: Mapped[list[str]] = mapped_column(JSONB, default=[], nullable=True)
    position: Mapped[int] = mapped_column(Integer())
    due_date: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())

    columns: Mapped[Column] = relationship(
        back_populates="cards",
        viewonly=True,
    )

    priority: Mapped[PriorityEnum] = mapped_column(String(), server_default=PriorityEnum.LOW.value)

    reporter_id: Mapped[UUID] = mapped_column(ForeignKey("user_account.id"), nullable=False)
    reporter: Mapped[User] = relationship(
        "User",
        foreign_keys=[reporter_id],
        lazy="selectin",
    )

    assignees: Mapped[list[User]] = relationship(
        secondary=lambda: card_assignee,
        back_populates="assigned_cards",
        lazy="selectin",
        cascade="all, delete",
        passive_deletes=True,
    )
