from pydantic import BaseModel
from tortoise.models import Model
from tortoise import fields
from datetime import datetime
from typing import Union, Optional


class Nooha(Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=255)
    authors = fields.TextField()
    aws_key = fields.CharField(max_length=255, null=True, default=None)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(null=True)
    uploaded_at = fields.DatetimeField(null=True)
    categories = fields.ManyToManyField('models.Category')


class NoohaResponse(BaseModel):
    id: int
    title: str
    authors: str
    aws_key: Union[str, None] = None
    created_at: datetime
    updated_at: Union[datetime, None] = None
    uploaded_at:  Union[datetime, None] = None
    categories: list[int] = []


class NoohaCreate(BaseModel):
    title: str
    authors: str
    categories: Optional[list[int]] = None


class NoohaEdit(BaseModel):
    title: Optional[str] = None
    authors: Optional[str] = None
    categories: Optional[list[int]] = None
    