from pydantic import BaseModel, Field
from tortoise.models import Model
from tortoise import fields
from typing import Union
from datetime import datetime


class Category(Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=255, unique=True, db_index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(null=True)


class CategoryResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: Union[datetime, None] = None


class CreateCategory(BaseModel):
    title: str = Field(min_length=5)

class EditCategory(CreateCategory):
    pass