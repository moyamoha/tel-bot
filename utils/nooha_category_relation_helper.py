from models.nooha_category import NoohaCategory
from models.nooha import Nooha, NoohaResponse
from models.category import Category
from typing import Sequence


async def edit_nooha_categories(nooha: Nooha, categories: list[int] | None = None):
    if categories is not None:
        relations = await NoohaCategory.filter(nooha_id=id)
        for rel in relations:
            await rel.delete()
        for _id in categories:
            category = await Category.get_or_none(id=_id)
            if category is None:
                continue
            nc = NoohaCategory(nooha=nooha, category=category)
            await nc.save()

async def create_nooha_categories(nooha: Nooha, categories: list[int] | None = None):
    added_category_ids = []
    if categories is not None:
        for _id in categories:
            category = await Category.get_or_none(id=_id)
            if category is None:
                continue
            nc = NoohaCategory(nooha=nooha, category=category)
            await nc.save()
            added_category_ids.append(_id)
    return added_category_ids

def nooha_orm_to_nooha_response(nooha: Nooha, categories: list[int] = []):
    result = NoohaResponse(
        id=nooha.id,
        title= nooha.title,
        authors=nooha.authors,
        aws_key=nooha.aws_key,
        created_at=nooha.created_at,
        updated_at=nooha.updated_at,
        uploaded_at=nooha.uploaded_at,
        categories=categories
    )
    return result

async def bulk_nooha_orm_to_nooha_response(data: list[Nooha]):
    result = []
    for n in data:
        relations = await NoohaCategory.filter(nooha_id=n.id)
        result.append(nooha_orm_to_nooha_response(n, categories=[rel.category_id for rel in relations]))
    return result