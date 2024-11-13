from pydantic import BaseModel, Field, constr
from tortoise.models import Model
from tortoise import fields
from pydantic.types import StringConstraints
from datetime import datetime
from typing import Union, Optional, Annotated
from re import RegexFlag

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

class NoohaListResponse(BaseModel):
    total_count: int
    items: list[NoohaResponse]


class NoohaCreate(BaseModel):
    title: str = Field(min_length=5)
    authors: str = Field(min_length=5)
    categories: Optional[list[int]] = None


class NoohaEdit(BaseModel):
    title: Optional[Annotated[str, StringConstraints(min_length=5)]] = None
    authors: Optional[Annotated[str, StringConstraints(min_length=5)]] = None
    categories: Optional[list[int]] = None
    