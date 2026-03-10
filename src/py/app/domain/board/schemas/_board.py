from uuid import UUID
from datetime import datetime
from app.lib.schema import CamelizedBaseStruct


class Board(CamelizedBaseStruct):
    owner_id: UUID
    title: str
    bg_color: str
    id: UUID
    created_at: datetime
    updated_at: datetime


class CreateBoard(CamelizedBaseStruct):
    owner_id: UUID
    title: str
    bg_color: str
