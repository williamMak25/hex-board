from datetime import datetime
from uuid import UUID

from app.lib.schema import CamelizedBaseStruct


class Column(CamelizedBaseStruct):
    board_id: UUID
    title: str
    col_position: int

    id: UUID
    created_at: datetime
    updated_at: datetime


class CreateColumn(CamelizedBaseStruct):
    board_id: UUID
    title: str
    # col_position: int
    

class UpdateColumnTitle(CamelizedBaseStruct):
    title: str

class UpdateColumnPosition(CamelizedBaseStruct):
    board_id: UUID
    col_position:int