from __future__ import annotations

from advanced_alchemy import repository, service

from app.db import models as m
from app.lib.service import AutoSlugServiceMixin


class BoardService(AutoSlugServiceMixin[m.Board], service.SQLAlchemyAsyncRepositoryService[m.Board]):
    """Handles basic lookup operations for an Tag."""

    class Repo(repository.SQLAlchemyAsyncSlugRepository[m.Board]):
        """Tag Repository."""

        model_type = m.Board

    repository_type = Repo
    match_fields = ["title"]
