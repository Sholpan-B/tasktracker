from typing import Any, Dict

from fastapi.exceptions import HTTPException
from starlette import status


class BaseHTTPException(HTTPException):
    pass


class HTTPBadRequestException(BaseHTTPException):
    def __init__(
        self, status_code: int = status.HTTP_400_BAD_REQUEST, detail: Any = None,
            headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class HTTPNotFoundException(BaseHTTPException):
    def __init__(
        self, status_code: int = status.HTTP_404_NOT_FOUND, detail: Any = None,
            headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
