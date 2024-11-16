from fastapi import APIRouter, status
from datetime import datetime
from models.category import Category, CreateCategory, EditCategory, CategoryResponse
from utils.nooha_category_relation_helper import category_orm_to_category_response

category_router = APIRouter(prefix="/categories", tags=["Nooha Categories"])

@category_router.get("/", response_model=list[CategoryResponse])
async def get_categories():
    categs = await Category.all()
    result = []
    for c in categs:
        result.append(await category_orm_to_category_response(c))
    return result

@category_router.get("/{id}", response_model=CategoryResponse)
async def get_categories(id: int):
    c = await Category.get(id=id)
    return await category_orm_to_category_response(category=c)

@category_router.post("/", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
async def create_category(category: CreateCategory):
    c = await Category.create(**category.model_dump())
    await c.save()
    return await category_orm_to_category_response(c, just_created=True)

@category_router.put("/{id}", response_model=CategoryResponse)
async def edit_category(id: int, category: EditCategory):
    c = await Category.get(id=id)
    await c.update_from_dict(category.model_dump())
    c.updated_at = datetime.now()
    await c.save()
    return await category_orm_to_category_response(c)

@category_router.delete("/{id}")
async def delete_category(id: int):
    c = await Category.get(id=id)
    await c.delete()