from uuid import UUID

import fastapi
from fastapi import APIRouter

import src.app.exceptions.common as common_exc
import src.app.exceptions.http as http_exc
from src.app.api.schemas import TaskSchema, TaskGetSchema
from src.app.db.repository import TaskRepository

# 'api/task':
router = APIRouter(prefix='/task')
repo = TaskRepository()


# Контроллер:
@router.get('')
async def get_tasks(query: TaskGetSchema = fastapi.Depends()):
    return await repo.get_list(**query.model_dump())


@router.get('/{id}')
async def get_task(id: UUID):
    try:
        return await repo.get(id)
    except common_exc.NotFoundException as e:
        raise http_exc.HTTPNotFoundException(detail=str(e))


@router.post('')
async def create_task(body: TaskSchema):
    try:
        return await repo.create(**body.model_dump())

    except common_exc.CreateException as e:
        raise http_exc.HTTPBadRequestException(detail=str(e))

    except common_exc.NotFoundException as e:
        raise http_exc.HTTPNotFoundException(detail=str(e))


@router.patch('/{id}')
async def update_task(id: UUID, body: TaskSchema):
    try:
        return await repo.update(id, **body.model_dump())

    except common_exc.UpdateException as e:
        raise http_exc.HTTPBadRequestException(detail=str(e))

    except common_exc.NotFoundException as e:
        raise http_exc.HTTPNotFoundException(detail=str(e))


@router.delete('/{id}')
async def delete_task(id: UUID, body: TaskSchema):
    try:
        return await repo.delete(id)

    except common_exc.DeleteException as e:
        raise http_exc.HTTPBadRequestException(detail=str(e))

    except common_exc.NotFoundException as e:
        raise http_exc.HTTPNotFoundException(detail=str(e))
