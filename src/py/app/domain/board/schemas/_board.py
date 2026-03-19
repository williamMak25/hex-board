from uuid import UUID
from datetime import datetime
from app.lib.schema import CamelizedBaseStruct
from app.domain.accounts.schemas import User

class Board(CamelizedBaseStruct):
    owner_id: UUID
    title: str
    bg_color: str
    id: UUID
    created_at: datetime
    updated_at: datetime
    members:list[User]


class CreateBoard(CamelizedBaseStruct):
    owner_id: UUID
    title: str
    bg_color: str
    member_ids:list[UUID] = []
