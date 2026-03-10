from app.lib.service import AutoSlugServiceMixin
from advanced_alchemy import repository,service
from app.db import models as m

class CardService(AutoSlugServiceMixin[m.Card],service.SQLAlchemyAsyncRepositoryService[m.Card]):

    class Repo(repository.SQLAlchemyAsyncRepository[m.Card]):
        model_type = m.Card
    repository_type = Repo

    match_fields = "title"