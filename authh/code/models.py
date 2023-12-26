import datetime

from tortoise import fields, models


class User(models.Model):
    id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=100)
    name = fields.CharField(max_length=100)
    surname = fields.CharField(max_length=100)
    email = fields.CharField(max_length=200, unique=True)
    password = fields.CharField(max_length=300)
    date_registered = fields.DateField(auto_now_add=True)

    class Meta:
        table = 'user'

    def __str__(self):
        return self.username

