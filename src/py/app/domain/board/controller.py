from typing import Annotated
from uuid import UUID

# if TYPE_CHECKING:
from advanced_alchemy.filters import FilterTypes
from advanced_alchemy.service.pagination import OffsetPagination
from litestar import Controller, get, post
from litestar.params import Dependency

from app.domain.board.schemas import Board, CreateBoard
from app.domain.board.service import BoardService
from app.lib.deps import create_service_dependencies


class BoardController(Controller):
    tags = ["Board"]
    path = "/api/boards"
    dependencies = create_service_dependencies(
        BoardService,
        key="board_service",
        filters={
            "id_filter": UUID,
            "search": "title",
            "pagination_type": "limit_offset",
            "pagination_size": 20,
            "created_at": True,
            "updated_at": True,
            "sort_field": "title",
            "sort_order": "asc",
        },
    )

    @get(operation_id="List Board", path="/")
    async def board_list(
        self,
        board_service: BoardService,
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[Board]:
        result, total = await board_service.list_and_count(*filters)

        return board_service.to_schema(data=result, total=total, schema_type=Board)

    @post(operation_id="", path="/create")
    async def create_board(self, board_service: BoardService, data: CreateBoard) -> Board:
        db_obj = await board_service.create(data.to_dict())
        return board_service.to_schema(db_obj, schema_type=Board)
