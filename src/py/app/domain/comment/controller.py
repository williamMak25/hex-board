from uuid import UUID

from litestar import Controller, websocket_listener, WebSocket

from app.domain.comment.service import CommentService
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

    @websocket_listener("/")
    async def handler(self, comment_service: CommentService, data: str, socket: WebSocket) -> str:
        if data == "goodbye":
            await socket.close()
        return data
