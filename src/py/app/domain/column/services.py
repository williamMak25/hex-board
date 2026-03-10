from app.lib.service import AutoSlugServiceMixin
from app.db import models as m
from advanced_alchemy import repository,service


class ColumnService(AutoSlugServiceMixin[m.Column], service.SQLAlchemyAsyncRepositoryService[m.Column]):

    class Repo(repository.SQLAlchemyAsyncRepository[m.Column]):
        model_type = m.Column

    repository_type = Repo
    match_fields = "title"