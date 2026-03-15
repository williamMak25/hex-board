from datetime import datetime
from uuid import UUID

from app.domain.accounts.schemas import User
from app.lib.schema import CamelizedBaseStruct
from app.lib.schema import PriorityEnum



class Card(CamelizedBaseStruct):
    col_id: UUID
    title: str
    description: str
    position: int
    due_date: datetime
    
    priority: PriorityEnum
    reporter_id: UUID
    reporter: User | None
    id: UUID
    created_at: datetime
    updated_at: datetime
    assignees: list[User] = []
    attachements: list[str] | None = None
    class Config:
        orm_mode = True


class CreateCard(CamelizedBaseStruct):
    col_id: UUID
    title: str
    description: str
    due_date: datetime
    priority: PriorityEnum
    reporter_id: UUID
    assignee_ids: list[UUID] = []
    attachements: list[str] | None = None

class UpdateCardPosition(CamelizedBaseStruct):
    col_id: UUID
    position: int
