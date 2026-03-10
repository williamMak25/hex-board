from typing import Annotated
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from advanced_alchemy.service.pagination import OffsetPagination
from litestar import Controller, get, post
from litestar.params import Dependency

from app.domain.cards.schemas import Card, CreateCard
from app.domain.cards.services import CardService
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

    @get(operation_id="Column Card List", path="/list")
    async def card_list(
        self,
        card_service: CardService,
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[Card]:
        results, total = await card_service.list_and_count(*filters)
        return card_service.to_schema(data=results, total=total, schema_type=Card)

    @post(operation_id="Create Column Card", path="/create")
    async def create_column_card(self, card_service: CardService, data: CreateCard) -> Card:
        db_obj = await card_service.create(data.to_dict())
        return card_service.to_schema(db_obj, schema_type=Card)
