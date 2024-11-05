from pydantic import BaseModel
from tortoise.models import Model
from tortoise import fields
from datetime import datetime


class Nooha(Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=255)
    authors = fields.TextField()
    aws_key = fields.CharField(max_length=255, null=True, default=None)
    created_at = fields.DatetimeField(default=datetime.now())
    updated_at = fields.DatetimeField(null=True)
    uploaded_at = fields.DatetimeField(null=True)


class NoohaCreate(BaseModel):
    title: str
    authors: str