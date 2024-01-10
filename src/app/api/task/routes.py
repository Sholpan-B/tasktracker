from typing import List
from uuid import UUID
from starlette import status
import fastapi as fa
from api import schemas

import exceptions.common as common_exc
import exceptions.http as http_exc

from db.repository import TaskRepository

from db import models

# 'api/task':
router = fa.APIRouter(prefix='/task', tags=['task'])
repo = TaskRepository()


# Контроллер:
@router.get('')
async def get_tasks(query: schemas.TaskGetSchema = fa.Depends()):
    return await repo.get_list(**query.dict(exclude_none=True))


@router.get('/{id}')
async def get_task(id: UUID):
    try:
        return await repo.get(id)
    except common_exc.NotFoundException as e:
        raise http_exc.HTTPNotFoundException(detail=str(e))


@router.post('')
async def create_task(
    body: schemas.TaskSchema = fa.Depends(schemas.TaskSchema.as_form),
    avatar: fa.UploadFile = fa.File(...),
):
    try:
        return await repo.create(**body.dict(), avatar=avatar)

    except common_exc.CreateException as e:
        raise http_exc.HTTPBadRequestException(detail=str(e))

    except common_exc.NotFoundException as e:
        raise http_exc.HTTPNotFoundException(detail=str(e))


@router.patch('/{id}')
async def update_task(id: UUID, body: schemas.TaskUpdateSchema):
    try:
        return await repo.update(id, **body.dict(exclude_none=True))

    except common_exc.UpdateException as e:
        raise http_exc.HTTPBadRequestException(detail=str(e))

    except common_exc.NotFoundException as e:
        raise http_exc.HTTPNotFoundException(detail=str(e))


@router.delete('/{id}')
async def delete_task(id: UUID):
    try:
        await repo.delete(id)
        return fa.responses.Response(status_code=status.HTTP_204_NO_CONTENT)

    except common_exc.DeleteException as e:
        raise http_exc.HTTPBadRequestException(detail=str(e))

    except common_exc.NotFoundException as e:
        raise http_exc.HTTPNotFoundException(detail=str(e))


# Comments:
@router.post('/task/{task_id}/comment')
async def add_comment_to_task(task_id: UUID, text: str, author_id: UUID):
    try:
        return await repo.add_comment_to_task(task_id, text, author_id)
    except common_exc.NotFoundException as e:
        raise http_exc.HTTPNotFoundException(detail=str(e))


@router.get('/task/{task_id}/comments')
async def get_task_comments(task_id: UUID):
    return await repo.get_task_comments(task_id)


@router.delete('/comment/{comment_id}')
async def delete_comment(comment_id: UUID):
    try:
        await repo.delete_comment(comment_id)
        return fa.responses.Response(status_code=status.HTTP_204_NO_CONTENT)
    except common_exc.NotFoundException as e:
        raise http_exc.HTTPNotFoundException(detail=str(e))


# Categories:
@router.get('/categories', response_model=List[str])
async def get_categories():
    categories = await models.Task.values_list('category', flat=True).distinct()
    return categories
