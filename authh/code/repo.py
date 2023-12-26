from uuid import UUID
import tortoise
import tortoise.exceptions

import models
from src.app.exceptions import common as common_exc
from passlib.context import CryptContext


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


class UserRepo(BaseRepo):
    models = models.User

    @staticmethod
    def __get_password_hash(password: str):
        pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

        return pwd_context.hash(password)

    async def create(self, **kwargs) -> models.User:
        kwargs['password'] = self.__get_password_hash(kwargs['password'])
        return await super().create(**kwargs)
