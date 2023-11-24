import fastapi
import pydantic
from starlette import status
from fastapi.responses import JSONResponse

from .http import BaseHTTPException


async def query_params_exc_handler(
    request: fastapi.Request, exc: pydantic.ValidationError,
) -> JSONResponse:
    return JSONResponse(
        {'detail': exc.errors()}, status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def request_exc_handler(
    request: fastapi.Request, exc: BaseHTTPException,
) -> JSONResponse:
    return JSONResponse(
        {'detail': exc.detail}, exc.status_code,
    )


async def internal_exc_handler(
    request: fastapi.Request, exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        {'detail': 'Internal Server Error'}, status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
