from uuid import UUID
import tortoise
import tortoise.exceptions

from exceptions import common as common_exc
from db import models


class BaseRepo:
    model: tortoise.Model

    async def get_list(self, **kwargs) -> list[tortoise.Model]:
        return await self.model.filter(**kwargs)

    async def get(self, id: UUID) -> tortoise.Model:
        try:
            return await self.model.get(id=id)
        except tortoise.exceptions.DoesNotExist as e:
            raise common_exc.NotFoundException(str(e))

    async def create(self, **kwargs) -> tortoise.Model:
        kwargs.setdefault('status', 'new')
        try:
            return await self.model.create(**kwargs)
        except tortoise.exceptions.IntegrityError as e:
            raise common_exc.CreateException(str(e))

    async def update(self, id: UUID, **kwargs) -> tortoise.Model:
        try:
            instance = await self.get(id=id)
            await instance.update_from_dict(kwargs).save()

            return instance

        except tortoise.exceptions.IntegrityError as e:
            raise common_exc.UpdateException(str(e))

    async def delete(self, id: UUID) -> None:
        try:
            instance = await self.get(id=id)
            await instance.delete()

        except tortoise.exceptions.IntegrityError as e:
            raise common_exc.DeleteException(str(e))


class TaskRepository(BaseRepo):
    model = models.Task

    async def get_task_comments(self, task_id: UUID) -> list[models.Comment]:
        task = await self.get(id=task_id)
        return await task.comments

    async def add_comment_to_task(self, task_id: UUID, text: str, author_id: UUID) -> models.Comment:
        task = await self.get(id=task_id)
        author = await models.User.get(id=author_id)
        comment = await models.Comment.create(task=task, text=text, author=author)
        return comment

    async def delete_comment(self, comment_id: UUID) -> None:
        try:
            comment = await models.Comment.get(id=comment_id)
            await comment.delete()
        except tortoise.exceptions.DoesNotExist as e:
            raise common_exc.NotFoundException(str(e))

    async def assign_category(self, task_id: UUID, category: str) -> models.Task:
        try:
            task = await self.get(id=task_id)
            task.category = category
            await task.save()
            return task
        except tortoise.exceptions.DoesNotExist as e:
            raise common_exc.NotFoundException(str(e))
