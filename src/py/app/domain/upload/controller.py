from pathlib import Path
from uuid import UUID

import anyio
from litestar import Controller, enums, post
from litestar.datastructures import UploadFile
from litestar.params import Body

from app.domain.upload.schemas import CreateFile, FileType
from app.domain.upload.service import FileService
from app.lib.deps import create_service_dependencies
from app.lib.settings import AppSettings

UPLOAD_DIR = Path("./uploaded-files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class UploadController(Controller):
    tags = ["Upload Attachment"]
    path = "/api/file-upload"

    dependencies = create_service_dependencies(
        FileService,
        key="file_service",
        filters={
            "id_filter": UUID,
            "search": "file_name",
            "pagination_type": "limit_offset",
            "pagination_size": 20,
            "created_at": True,
            "updated_at": True,
            "sort_field": "file_name",
            "sort_order": "asc",
        },
    )

    @post(operation_id="File Upload")
    async def upload_file(
        self,
        settings: AppSettings,
        file_service: FileService,
        data: list[UploadFile] = Body(media_type=enums.RequestEncodingType.MULTI_PART),
    ) -> list[FileType]:
        
        files = []
        for input_file in data:

            file_path = UPLOAD_DIR / input_file.filename
            async with await anyio.Path(file_path).open("wb") as f:
                content = await input_file.read()
                await f.write(content)

                file = CreateFile(
                    file_name=input_file.filename,
                    size=len(content),
                    file_path=f"{settings.URL}/{file_path}",
                    file_type=input_file.filename.split(".")[-1],
                )

                db_obj = await file_service.create(file)
                upload_file = FileType(**db_obj.to_dict())
                files.append(upload_file)
        return files
