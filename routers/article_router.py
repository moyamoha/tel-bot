from fastapi.routing import APIRouter
from models.article import ArticleListResponse, Article, ArticleResponse, CreateArticle, EditArticle
from utils.article_utils import article_orm_to_article_response, bulk_article_orm_to_article_response


article_router = APIRouter(prefix='/articles', tags=['Articles'])

@article_router.get('/', response_model=ArticleListResponse)
async def get_articles(page: int = 1, per_page: int = 10):
    articles_query = Article.all()
    count = await articles_query.count()
    articles = await articles_query.offset((page - 1) * per_page).limit(per_page)
    return bulk_article_orm_to_article_response(articles, count)

@article_router.get('/{id}', response_model=ArticleResponse)
async def get_article(id: int):
    article = await Article.get(id=id)
    return article_orm_to_article_response(article)


@article_router.post('/', response_model=ArticleResponse)
async def create_article(article: CreateArticle):
    update_data = article.model_dump()
    if 'keywords' in update_data:
        if len(update_data['keywords']) == 0:
            update_data['keywords'] = None
        else:
            update_data['keywords'] = '|'.join(update_data['keywords'])
    b = await Article.create(**update_data)
    await b.save()
    return article_orm_to_article_response(b)

@article_router.put('/{id}')
async def update_article(id: int, article: EditArticle):
    a = await Article.get(id=id)
    article_as_dict = article.model_dump()
    update_data = {k: v for k, v in article_as_dict.items() if v is not None}
    if not update_data:
        return
    if 'keywords' in update_data:
        if len(update_data['keywords']) == 0:
            update_data['keywords'] = None
        else:
            update_data['keywords'] = '|'.join(update_data['keywords'])
    await a.update_from_dict(update_data)
    await a.save()

@article_router.delete('/{id}')
async def remove_article(id: int):
    article = await Article.get(id=id)
    await article.delete()