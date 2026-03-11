from app.lib.schema import CamelizedBaseStruct
from uuid import UUID
from datetime import datetime
class Card(CamelizedBaseStruct):
    col_id: UUID
    title: str
    description: str
    position: int
    due_date: datetime
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CreateCard(CamelizedBaseStruct):
    col_id: UUID
    title: str
    description: str
    due_date: datetime


class UpdateCardPosition(CamelizedBaseStruct):
    col_id: UUID
    position: int