from tortoise import models, fields
import custom_fields


class IdMixin(models.Model):
    id = fields.UUIDField(pk=True)

    class Meta:
        abstract = True


class TimeStampMixin(models.Model):
    created_at = fields.DatetimeField(auto_now=True)
    updated_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True


class BaseModel(IdMixin, TimeStampMixin):
    class Meta:
        abstract = True


class Tag(BaseModel):
    name = fields.CharField(max_length=100)
    tasks = fields.ManyToManyField('models.Task', related_name='tags')

    class Meta:
        table = 'tag'


class Task(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.TextField()
    description = fields.TextField()
    status = fields.CharField(max_length=20, choices=["in process", "done", "new"])
    author = fields.ForeignKeyField('models.User', related_name='tasks')
    category = fields.CharField(max_length=50)
    avatar = custom_fields.FileField(upload_to='media/avatars', null=True)

    class Meta:
        table = 'task'


# class User(models.Model):
#     id = fields.UUIDField(pk=True)
#     username = fields.CharField(unique=True, max_length=100)
#     password = fields.CharField(max_length=255)
#
#     class Meta:
#         table = 'user'


class Comment(BaseModel):
    id = fields.UUIDField(pk=True)
    task = fields.ForeignKeyField('models.Task', related_name='comments')
    text = fields.TextField()
    author = fields.ForeignKeyField('models.User', related_name='comments')
