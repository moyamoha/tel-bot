from fastapi import APIRouter, status
from datetime import datetime
from models.category import Category, CreateCategory, EditCategory, CategoryResponse


category_router = APIRouter(prefix="/categories", tags=["Nooha Categories"])

@category_router.get("/", response_model=list[CategoryResponse])
async def get_categories():
    categs = await Category.all()
    return categs

@category_router.get("/{id}", response_model=CategoryResponse)
async def get_categories(id: int):
    c = await Category.get(id=id)
    return c

@category_router.post("/", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
async def create_category(category: CreateCategory):
    c = await Category.create(**category.model_dump())
    await c.save()
    return c

@category_router.put("/{id}", response_model=CategoryResponse)
async def edit_category(id: int, category: EditCategory):
    c = await Category.get(id=id)
    await c.update_from_dict(category.model_dump())
    c.updated_at = datetime.now()
    await c.save()
    return c

@category_router.delete("/{id}")
async def delete_category(id: int):
    c = await Category.get(id=id)
    await c.delete()