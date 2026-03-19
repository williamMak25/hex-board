from sqlalchemy import Table,Column,ForeignKey,UUID
from advanced_alchemy.base import orm_registry


board_member = Table(
    "board_member",
    orm_registry.metadata,
    Column("board_id",UUID(as_uuid=True), ForeignKey("board.id"),primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("user_account.id"),primary_key=True)
)