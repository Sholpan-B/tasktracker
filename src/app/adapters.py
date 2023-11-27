import io
import settings
import fastapi

from minio import Minio


class MinIOClient(Minio):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            endpoint=settings.minio_url,
            access_key=settings.minio_root_user,
            secret_key=settings.minio_root_password,
            secure=False,
            **kwargs,
        )

    async def upload_from_bytes(self, file: fastapi.UploadFile) -> None:
        file_data = await file.read()

        self.put_object(
            bucket_name=settings.minio_bucket_name,
            object_name=file.filename,
            data=io.BytesIO(file_data),
            length=len(file_data),
        )
