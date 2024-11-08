from fastapi.routing import APIRouter
from fastapi import status, UploadFile, HTTPException
from models.nooha import Nooha, NoohaCreate, NoohaEdit, NoohaResponse
from models.category import Category
from models.nooha_category import NoohaCategory
from di_container import AppContainer
from datetime import datetime
from typing import Union
from utils.nooha_category_relation_helper import create_nooha_categories, \
    edit_nooha_categories, \
    nooha_orm_to_nooha_response, \
    bulk_nooha_orm_to_nooha_response


router = APIRouter(prefix="/noohas", tags=["Noohas"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=NoohaResponse)
async def create_nooha(nooha: NoohaCreate):
    nooha_as_dict = nooha.model_dump()
    # category_ids = nooha_as_dict.get("categories")
    category_ids = nooha_as_dict.pop("categories")
    n = await Nooha.create(**nooha_as_dict)
    added_category_ids = await create_nooha_categories(n, categories=category_ids)
    await n.save()
    await Nooha
    return nooha_orm_to_nooha_response(n, categories=added_category_ids)

@router.put('/upload/{id}')
async def upload_nooha(id: int, file: UploadFile):
    n = await Nooha.get(id=id)
    nooha_storage = AppContainer().nooha_storage()
    try:
        key = nooha_storage.upload_nooha(file, nooha=n)
        n.aws_key = key
        if n.uploaded_at is None:
            n.uploaded_at = datetime.now()
        await n.save()
    except Exception as e:
        print(e)

@router.get("/", response_model=list[NoohaResponse])
async def get_noohas(category_title: Union[str, None] = None):
    if not category_title:
        noohas = await Nooha.all()
        return await bulk_nooha_orm_to_nooha_response(noohas)
    else:
        category = await Category.get_or_none(title=category_title)
        if not category:
            raise HTTPException(404, detail=f'{category_title} was not found')
        noohas = await Nooha.filter(categories=category).prefetch_related('categories')
        return await bulk_nooha_orm_to_nooha_response(noohas)

@router.get("/{id}")
async def get_single_nooha(id: int, response_model=NoohaResponse):
    nooha = await Nooha.get(id=id)
    relations = await NoohaCategory.filter(nooha=nooha)
    # print(relations)
    return nooha_orm_to_nooha_response(nooha, categories=[rel.category_id for rel in relations])

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=NoohaResponse)
async def edit_nooha(id: int, nooha: NoohaEdit):
    n = await Nooha.get(id=id)
    await edit_nooha_categories(n, nooha.categories)
    update_data = {k: v for k, v in nooha.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    await n.update_from_dict(update_data)
    n.updated_at = datetime.now()
    await n.save()
    return n



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_single_nooha(id: int):
    n = await Nooha.get(id=id)
    if n and n.aws_key:
        nooha_storage = AppContainer().nooha_storage()
        nooha_storage.delete_nooha(n.aws_key)
    await n.delete()
    # await NoohaCategory.raw(f"delete from nooha_category where nooha_id={id}")