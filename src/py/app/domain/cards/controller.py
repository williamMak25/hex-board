from typing import Annotated
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from advanced_alchemy.service.pagination import OffsetPagination
from litestar import Controller, get, patch, post, patch
from litestar.exceptions import NotFoundException
from litestar.params import Dependency

from app.domain.cards.schemas import Card, CreateCard, UpdateCardPosition
from app.domain.cards.services import CardService
from app.domain.column.services import ColumnService
from app.domain.accounts.services import UserService
from app.lib.deps import create_service_dependencies


class CardController(Controller):
    tags = ["Column Cards"]
    path = "/api/cards"

    dependencies = create_service_dependencies(
        CardService,
        key="card_service",
        filters={
            "id_filter": UUID,
            "search": "title",
            "pagination_type": "limit_offset",
            "pagination_size": 20,
            "created_at": True,
            "updated_at": True,
            "sort_field": "position",
            "sort_order": "asc",
        },
    )
    dependencies.update(create_service_dependencies(ColumnService, key="column_service", filters={"id_filter": UUID}))
    dependencies.update(create_service_dependencies(UserService, key="user_service", filters={"id_filter": UUID}))

    @get(operation_id="Column Card List", path="/list")
    async def card_list(
        self,
        card_service: CardService,
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[Card]:
        results, total = await card_service.list_and_count(*filters)
        return card_service.to_schema(data=results, total=total, schema_type=Card)
    
    @patch(operation_id="Card Update", path="/update/{card_id:uuid}")
    async def update_card(self, card_id: UUID, card_service: CardService, data: CreateCard) -> Card:
        db_obj = await card_service.update(item_id=card_id, data=data.to_dict())
        return card_service.to_schema(db_obj, schema_type=Card)

    @get(operation_id="Get Column Card", path="/column-cards/{column_id:uuid}")
    async def get_column_card(self, column_id: UUID, card_service: CardService) -> list[dict[str, str]]:
        db_obj = await card_service.list(col_id=column_id)

        return [c.to_dict() for c in db_obj if len(db_obj) > 0]

    @post(operation_id="Create Column Card", path="/create")
    async def create_column_card(self, card_service: CardService, user_service: UserService, data: CreateCard) -> Card:

        create_data = data.to_dict()
        cards = await card_service.list(col_id=data.col_id)
        create_data["position"] = len(cards) if cards else 0
        all_user = await user_service.list()

        assigned_users = [user for user in all_user if user.id in data.assignee_ids]
        create_data["assignees"] = assigned_users

        create_data.pop("assignee_ids", None)

        db_obj = await card_service.create(create_data)
        await card_service.repository.session.refresh(db_obj)
        return card_service.to_schema(db_obj, schema_type=Card)

    @patch(operation_id="Move Column Card Position", path="/card-position/{card_id:uuid}")
    async def move_column_card_position(
        self, card_id: UUID, card_service: CardService, column_service: ColumnService, data: UpdateCardPosition
    ) -> None:
        col = await column_service.get_one_or_none(id=data.col_id)
        if not col:
            raise NotFoundException(detail="Column not found", status_code=404)
        cards = await card_service.list(col_id=col.id)

        if len(cards) == 0:
            card = await card_service.get_one_or_none(id=card_id)
            if not card:
                raise NotFoundException(detail="Card not found", status_code=404)
            card.position = 0
            card.col_id = col.id
            await card_service.update(card)
        else:
            target_card = await card_service.get_one_or_none(id=card_id)

            other_cards = [card for card in cards if card.id != card_id]

            other_cards.sort(key=lambda x: x.position)
            new_index = max(0, min(data.position, len(other_cards)))

            if target_card:
                target_card.col_id = data.col_id
                other_cards.insert(new_index, target_card)

            for index, card in enumerate(other_cards):
                card.position = index

            await card_service.update_many(other_cards)
        await card_service.repository.session.commit()

    @get(operation_id="Get Column Card Detail", path="/detail/{card_id:uuid}")
    async def get_column_card_detail(self, card_id: UUID, card_service: CardService) -> Card:
        db_obj = await card_service.get_one_or_none(id=card_id)
        if not db_obj:
            raise NotFoundException(detail="Card not found", status_code=404)
        return card_service.to_schema(db_obj, schema_type=Card)
