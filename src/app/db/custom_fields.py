import os
import typing
from typing import Any
import uuid
from datetime import datetime
from pathlib import Path

from starlette.datastructures import UploadFile
from tortoise.fields import TextField


def get_valid_filename(name: str):
    return str(name).strip().replace(' ', '_').replace('..', '')


class FileField(TextField):
    def __init__(self, *, upload_to: str, **kwargs) -> None:
        super().__init__(**kwargs)
        upload_to = datetime.now().strftime(upload_to)

        if not os.path.exists(upload_to):
            os.makedirs(upload_to, exist_ok=True)

        self.upload_to = Path(upload_to)

    def to_db_value(self, value: str | UploadFile | bytes, *args, **kwargs):
        if isinstance(value, UploadFile):
            return self.save_file(value)
        elif isinstance(value, str):
            return value
        return value

    def to_python_value(self, value: str | UploadFile | bytes, *args, **kwargs):
        if isinstance(value, str):
            return value
        elif isinstance(value, UploadFile):
            return self.save_file(value)

    def save_file(self, value: UploadFile):
        file = value.file
        file_name = get_valid_filename(value.filename)
        file_path = self.upload_to / file_name

        if os.path.isfile(file_path):
            file_path = self.upload_to / f'{uuid.uuid4()}-{file_name}'

        with open(file_path, 'wb') as f:
            f.write(file.read())

        return str(file_path)
    