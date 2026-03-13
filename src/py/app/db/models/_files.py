from advanced_alchemy.base import UUIDv7AuditBase
from sqlalchemy.orm import mapped_column , Mapped
from sqlalchemy import String, Float


class File(UUIDv7AuditBase):
    __tablename__ = "files"

    file_name: Mapped[str] = mapped_column(String, nullable=False, server_default="")
    file_path: Mapped[str] = mapped_column(String, nullable=False, server_default="")
    size: Mapped[float] = mapped_column(Float, nullable=False, server_default="0.0")
    file_type: Mapped[str] = mapped_column(String, nullable=False)