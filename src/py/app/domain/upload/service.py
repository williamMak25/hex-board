from app.lib.service import AutoSlugServiceMixin
from advanced_alchemy import service, repository
from app.db import models as m

class FileService(AutoSlugServiceMixin[m.File], service.SQLAlchemyAsyncRepositoryService[m.File]):

    class Repo(repository.SQLAlchemyAsyncRepository[m.File]):
        model_type = m.File

    repository_type = Repo