from __future__ import annotations

from app.lib.service import AutoSlugServiceMixin
from advanced_alchemy import repository,service
from app.db.models._card import Card

class CardService(AutoSlugServiceMixin[Card], service.SQLAlchemyAsyncRepositoryService[Card]):

    class Repo(repository.SQLAlchemyAsyncRepository[Card]):
        model_type = Card
    repository_type = Repo

    match_fields = "title"
    