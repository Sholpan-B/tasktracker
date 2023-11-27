from uuid import UUID
from starlette import status
import fastapi
from api import schemas

import exceptions.common as common_exc
import exceptions.http as http_exc

from db.repository import TaskRepository

# 'api/task':
router = fastapi.APIRouter(prefix='/task', tags=['task'])
repo = TaskRepository()


# Контроллер:
@router.get('')
async def get_tasks(query: schemas.TaskGetSchema = fastapi.Depends()):
    return await repo.get_list(**query.model_dump(exclude_none=True))


@router.get('/{id}')
async def get_task(id: UUID):
    try:
        return await repo.get(id)
    except common_exc.NotFoundException as e:
        raise http_exc.HTTPNotFoundException(detail=str(e))


@router.post('')
async def create_task(body: schemas.TaskSchema):
    try:
        return await repo.create(**body.model_dump(exclude_none=True))

    except common_exc.CreateException as e:
        raise http_exc.HTTPBadRequestException(detail=str(e))

    except common_exc.NotFoundException as e:
        raise http_exc.HTTPNotFoundException(detail=str(e))


@router.patch('/{id}')
async def update_task(id: UUID, body: schemas.TaskUpdateSchema):
    try:
        return await repo.update(id, **body.model_dump(exclude_none=True))

    except common_exc.UpdateException as e:
        raise http_exc.HTTPBadRequestException(detail=str(e))

    except common_exc.NotFoundException as e:
        raise http_exc.HTTPNotFoundException(detail=str(e))


@router.delete('/{id}')
async def delete_task(id: UUID):
    try:
        await repo.delete(id)
        return fastapi.responses.Response(status_code=status.HTTP_204_NO_CONTENT)

    except common_exc.DeleteException as e:
        raise http_exc.HTTPBadRequestException(detail=str(e))

    except common_exc.NotFoundException as e:
        raise http_exc.HTTPNotFoundException(detail=str(e))
