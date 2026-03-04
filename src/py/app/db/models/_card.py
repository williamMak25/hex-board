from sqlalchemy.orm import Mapped, mapped_column
from advanced_alchemy.base import UUIDv7AuditBase
from sqlalchemy import String, ForeignKey,Integer,DateTime,func
from uuid import UUID
from datetime import datetime

class Card(UUIDv7AuditBase):
    __tablename__ = 'card'

    col_id: Mapped[UUID] = mapped_column(ForeignKey("column.id",ondelete="CASCADE"),nullable=False)
    title:Mapped[str] = mapped_column(String())
    description:Mapped[str] = mapped_column(String())
    position:Mapped[int] = mapped_column(Integer())
    due_date: Mapped[datetime] = mapped_column(DateTime(),server_default=func.now())