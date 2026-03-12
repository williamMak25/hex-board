from typing import Annotated
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from advanced_alchemy.service.pagination import OffsetPagination
from litestar import Controller, get, patch, post
from litestar.exceptions import NotFoundException
from litestar.params import Dependency

from app.domain.cards.schemas import Card
from app.domain.accounts.schemas import User
from app.domain.column.schemas import Column, CreateColumn, UpdateColumnPosition, UpdateColumnTitle
from app.domain.column.services import ColumnService
from app.lib.deps import create_service_dependencies


class ColumnController(Controller):
    tags = ["Board  Column"]
    path = "/api/columns"

    dependencies = create_service_dependencies(
        ColumnService,
        key="column_service",
        filters={
            "id_filter": UUID,
            "search": "title",
            "pagination_type": "limit_offset",
            "pagination_size": 20,
            "created_at": True,
            "updated_at": True,
            "sort_field": "col_position",
            "sort_order": "asc",
        },
    )

    @get(operation_id="Board Column List", path="/list")
    async def column_list(
        self,
        column_service: ColumnService,
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[Column]:

        results, total = await column_service.list_and_count(*filters)
        return column_service.to_schema(data=results, total=total, schema_type=Column)

    @post(operation_id="Creat Board Column", path="/create")
    async def create_board_column(self, column_service: ColumnService, data: CreateColumn) -> Column:

        existing_columns = await column_service.list(board_id=data.board_id)
        create_data = data.to_dict()

        create_data["col_position"] = len(existing_columns) if existing_columns else 0
        db_obj = await column_service.create(create_data)
        return column_service.to_schema(db_obj, schema_type=Column)

    @patch(operation_id="Update Board Column", path="/{column_id:uuid}")
    async def update_column_title(
        self, column_id: UUID, column_service: ColumnService, data: UpdateColumnTitle
    ) -> Column:

        db_obj = await column_service.get_one_or_none(id=column_id)

        if not db_obj:
            raise NotFoundException(detail="No Column Found.", status_code=404)

        db_obj.title = data.title
        new_obj = await column_service.update(db_obj)

        return column_service.to_schema(new_obj, schema_type=Column)

    @patch(operation_id="Update Column Position", path="/col-position/{column_id:uuid}")
    async def update_column_position(
        self, column_id: UUID, column_service: ColumnService, data: UpdateColumnPosition
    ) -> None:
        columns = await column_service.list(board_id=data.board_id)

        if not columns:
            raise NotFoundException(detail="No Columns Found for this Board", status_code=404)

        target_col = next((c for c in columns if c.id == column_id), None)
        if not target_col:
            raise NotFoundException(detail="Column not found on this board", status_code=404)

        other_cols = [c for c in columns if c.id != column_id]

        other_cols.sort(key=lambda x: x.col_position)

        new_index = max(0, min(data.col_position, len(other_cols)))
        other_cols.insert(new_index, target_col)

        for index, col in enumerate(other_cols):
            col.col_position = index

        await column_service.update_many(other_cols)

    @get(operation_id="Get Board Column", path="/{board_id:uuid}")
    async def get_column(self, board_id: UUID, column_service: ColumnService) -> list[Column]:
        db_objs = await column_service.list(board_id=board_id)

        return [
            Column(
                id=col.id,
                board_id=col.board_id,
                title=col.title,
                col_position=col.col_position,
                created_at=col.created_at,
                updated_at=col.updated_at,
                cards=[
                    Card(
                        id=card.id,
                        col_id=card.col_id,
                        title=card.title,
                        description=card.description,
                        position=card.position,
                        due_date=card.due_date,
                        created_at=card.created_at,
                        updated_at=card.updated_at,
                        priority=card.priority,
                        attachements=card.attachements,
                        assignees=[],
                        reporter=None,
                        reporter_id=card.reporter_id,
                    )
                    for card in col.cards
                ],
            )
            for col in db_objs
        ]
# [User(**asignee.to_dict()) for asignee in card.assignees]
# User(**card.reporter.to_dict())