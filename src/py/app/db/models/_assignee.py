from __future__ import annotations

from advanced_alchemy.base import orm_registry
from sqlalchemy import UUID, Column, ForeignKey, Table


card_assignee = Table(
    "card_assignee",
    orm_registry.metadata,
    Column("card_id", UUID(as_uuid=True), ForeignKey("card.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("user_account.id", ondelete="CASCADE"), primary_key=True),
)
