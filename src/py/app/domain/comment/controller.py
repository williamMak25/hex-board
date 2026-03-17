from uuid import UUID

from litestar import Controller, post, get
from litestar.exceptions import NotFoundException
from app.domain.comment.service import CommentService
from app.domain.comment.schemas import Comment, CreateComment
from app.lib.deps import create_service_dependencies


class CommentController(Controller):
    tags = ["Card Comments"]
    path = "/api/card-comments"

    dependencies = create_service_dependencies(
        CommentService,
        key="comment_service",
        filters={
            "id_filter": UUID,
            "pagination_type": "limit_offset",
            "pagination_size": 20,
            "created_at": True,
            "updated_at": True,
            "sort_field": "created_at",
            "sort_order": "asc",
        },
    )

    @post(operation_id="Create comment",path="/")
    async def create_comment(
        self,
        comment_service: CommentService,
        data: CreateComment,
    )->Comment:
        db_obj = await comment_service.create(data)
        return comment_service.to_schema(db_obj,schema_type=Comment)


    @get(operation_id="Get comment",path="/{comment_id:uuid}")
    async def get_comment(
        self,
        comment_id:UUID,
        comment_service:CommentService,
    )->Comment:
        db_obj = await comment_service.get_one_or_none(id = comment_id)
        if db_obj is None:
            raise NotFoundException(status_code=404,detail="Comment not found")
        return comment_service.to_schema(db_obj,schema_type=Comment)


    @get(operation_id="Get comments by card",path="/by-card/{card_id:uuid}")
    async def get_comment_by_card(
        self,
        card_id:UUID,
        comment_service:CommentService,
    )->list[Comment]:
        comments = await comment_service.list(card_id=card_id)

        return [comment_service.to_schema(comment, schema_type=Comment) for comment in comments if len(comments) > 0]
