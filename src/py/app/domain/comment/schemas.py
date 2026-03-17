from datetime import datetime
from uuid import UUID

from app.domain.accounts.schemas import User
from app.lib.schema import CamelizedBaseStruct


class Comment(CamelizedBaseStruct):
    message: str
    user_id: UUID
    id: UUID
    card_id: UUID
    created_at: datetime
    updated_at: datetime
    comment_user: User | None = None


class CreateComment(CamelizedBaseStruct):
    message: str
    user_id: UUID
    card_id: UUID
