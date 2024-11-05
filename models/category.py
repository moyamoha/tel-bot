from tortoise.models import Model
from tortoise import fields
from datetime import datetime


class Category(Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(default=datetime.now())
    updated_at = fields.DatetimeField(null=True)