from models.article import Article, ArticleResponse, ArticleListResponse


def article_orm_to_article_response(article: Article):
    if article.keywords is None:
        keywords_as_str_list = []
    else:
        keywords_as_str_list = article.keywords.split('|')
    return ArticleResponse(
        id=article.id,
        title=article.title,
        content=article.content,
        created_at=article.created_at,
        updated_at=article.updated_at,
        keywords=keywords_as_str_list
    )

def bulk_article_orm_to_article_response(articles: list[Article], total_count: int):
    return ArticleListResponse(
        total_count=total_count,
        items=[article_orm_to_article_response(article) for article in articles]
    )