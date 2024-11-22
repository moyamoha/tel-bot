from datetime import datetime
from tortoise.models import Model
from tortoise import fields
from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated, Optional, Union


class Blog(Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    keywords = fields.TextField(null=True) # A group of words separated by |


class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: Union[datetime, None] = None
    keywords: list[str]


class BlogListResponse(BaseModel):
    total_count: int
    items: list[BlogResponse]


class CreateBlog(BaseModel):
    title: str = Field(min_length=10)
    content: str = Field(min_length=100)
    keywords: list[str]


class EditBlog(BaseModel):
    title: Optional[Annotated[str, StringConstraints(min_length=10)]] = None
    content: Optional[Annotated[str, StringConstraints(min_length=100)]] = None
    keywords: Optional[list[str]] = None