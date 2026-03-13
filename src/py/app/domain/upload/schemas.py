from app.lib.schema import CamelizedBaseStruct
from uuid import UUID
from datetime import datetime


class FileType(CamelizedBaseStruct):
    file_name: str
    file_path: str
    size: float
    file_type: str

    id: UUID
    created_at: datetime
    updated_at: datetime


class CreateFile(CamelizedBaseStruct):
    file_name: str
    file_path: str
    size: float
    file_type: str
