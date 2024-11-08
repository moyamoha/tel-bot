from fastapi import status, APIRouter
from tortoise import query_utils
from models.nooha_category import NoohaCategory

nooha_category_relation_router = APIRouter(prefix="/nooha-categories", tags=["Nooha-Category Relation"])

@nooha_category_relation_router.get("/")
async def create_relation(category: int, ):
    pass