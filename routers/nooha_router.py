from fastapi.routing import APIRouter
from fastapi import status, UploadFile, HTTPException
from models.nooha import Nooha, NoohaCreate, NoohaEdit, NoohaResponse, NoohaListResponse
from models.nooha_category import NoohaCategory
from di_container import AppContainer
from datetime import datetime
from typing import Union
from utils.nooha_category_relation_helper import create_nooha_categories, \
    edit_nooha_categories, \
    nooha_orm_to_nooha_response, \
    bulk_nooha_or_to_nooha_list
from tortoise.expressions import Q


router = APIRouter(prefix="/noohas", tags=["Noohas"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=NoohaResponse)
async def create_nooha(nooha: NoohaCreate):
    nooha_as_dict = nooha.model_dump()
    # category_ids = nooha_as_dict.get("categories")
    category_ids = nooha_as_dict.pop("categories")
    n = await Nooha.create(**nooha_as_dict)
    added_category_ids = await create_nooha_categories(n, categories=category_ids)
    await n.save()
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

@router.get("/", response_model=NoohaListResponse)
async def get_noohas(
        category_title: Union[str, None] = None,
        search: str = "",
        page: int = 1,
        per_page: int = 20
    ):
    offset = (page - 1) * per_page
    if not category_title:
        noohas_q = Nooha.filter(Q(title__icontains=search) | Q(authors__icontains=search))
        count = await noohas_q.count()
        noohas = await noohas_q.offset(offset).limit(per_page)
        return await bulk_nooha_or_to_nooha_list(count, noohas)
    else:
        noohas_q = Nooha.filter(Q(title__icontains=search) | Q(authors__icontains=search), categories__title=category_title)\
                        .prefetch_related('categories')
        count = await noohas_q.count()
        noohas = await noohas_q.offset(offset).limit(per_page)
        return await bulk_nooha_or_to_nooha_list(count, noohas)

@router.get("/{id}", response_model=NoohaResponse)
async def get_single_nooha(id: int):
    nooha = await Nooha.get(id=id)
    relations = await NoohaCategory.filter(nooha=nooha)
    # print(relations)
    return nooha_orm_to_nooha_response(nooha, categories=[rel.category_id for rel in relations])

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def edit_nooha(id: int, nooha: NoohaEdit):
    n = await Nooha.get(id=id)
    await edit_nooha_categories(n, nooha.categories)
    update_data = {k: v for k, v in nooha.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    await n.update_from_dict(update_data)
    n.updated_at = datetime.now()
    await n.save()



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_single_nooha(id: int):
    n = await Nooha.get(id=id)
    if n and n.aws_key:
        nooha_storage = AppContainer().nooha_storage()
        nooha_storage.delete_nooha(n.aws_key)
    await n.delete()
    # await NoohaCategory.raw(f"delete from nooha_category where nooha_id={id}")