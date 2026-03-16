from advanced_alchemy import service, repository
from app.lib.service import AutoSlugServiceMixin
from app.db.models._comment import Comment


class CommentService(AutoSlugServiceMixin[Comment], service.SQLAlchemyAsyncRepositoryService[Comment]):

    class Repository(repository.SQLAlchemyAsyncRepository[Comment]):
        model_type = Comment

    repository_type = Repository
