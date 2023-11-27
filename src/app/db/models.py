from tortoise import models, fields


class Task(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.TextField()
    description = fields.TextField()
    status = fields.CharField(max_length=20, choices=["in process", "done", "new"])
