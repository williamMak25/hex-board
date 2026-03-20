from typing import Annotated
from uuid import UUID

# if TYPE_CHECKING:
from advanced_alchemy.filters import FilterTypes
from sqlalchemy import or_
from advanced_alchemy.service.pagination import OffsetPagination
from litestar import Controller, get, post,delete,patch
from litestar.params import Dependency
from app.db import models as m
from app.domain.board.schemas import Board, CreateBoard
from app.domain.board.service import BoardService
from app.lib.deps import create_service_dependencies
from app.domain.accounts.services import UserService
from app.db.models._user import User
from litestar.exceptions import NotFoundException

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

    dependencies.update(create_service_dependencies(
        UserService,
        key="user_service"
    ))

    @get(operation_id="List Board", path="/")
    async def board_list(
        self,
        board_service: BoardService,
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
        current_user:User
    ) -> OffsetPagination[Board]:
        print(current_user.name)
        if current_user:
            filters.append(or_(m.Board.members.any(User.id == current_user.id), m.Board.owner_id == current_user.id))
        result, total = await board_service.list_and_count(*filters)

        return board_service.to_schema(data=result, total=total, schema_type=Board)

    @post(operation_id="Create Board", path="/create")
    async def create_board(self, board_service: BoardService,user_service:UserService, data: CreateBoard) -> Board:
        create_obj = data.to_dict()
        users = await user_service.list()
        members = [user for user in users if user.id in data.member_ids]
        create_obj["members"] = members
        create_obj.pop("member_ids", None)
        db_obj = await board_service.create(create_obj)
        await board_service.repository.session.refresh(db_obj)
        return board_service.to_schema(db_obj, schema_type=Board)

    @patch(operation_id="Update Board", path="/{board_id:uuid}")
    async def update_board(
        self,
        board_id: UUID,
        board_service: BoardService,
        user_service:UserService,
        data: CreateBoard,
    ) -> Board:
        board = await board_service.get_one_or_none(id=board_id)
        
        if not board:
            raise NotFoundException(detail="No Board Found.", status_code=404)
        board.title = data.title
        board.bg_color = data.bg_color
        users = await user_service.list()
        members = [user for user in users if user.id in data.member_ids]
        board.members = members
        db_obj = await board_service.update(board)
        return board_service.to_schema(db_obj, schema_type=Board)


    @delete(operation_id="Delete Board", path="/{board_id:uuid}")
    async def delete_board(
        self,
        board_id: UUID,
        board_service: BoardService,
    ) -> None:
        _ = await board_service.delete(board_id)