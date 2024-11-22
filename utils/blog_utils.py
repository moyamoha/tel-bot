from models.blog import Blog, BlogResponse, BlogListResponse


def blog_orm_to_blog_response(blog: Blog):
    if blog.keywords is None:
        keywords_as_str_list = []
    else:
        keywords_as_str_list = blog.keywords.split('|')
    return BlogResponse(
        id=blog.id,
        title=blog.title,
        content=blog.content,
        created_at=blog.created_at,
        updated_at=blog.updated_at,
        keywords=keywords_as_str_list
    )

def bulk_blog_orm_to_blog_response(blogs: list[Blog], total_count: int):
    return BlogListResponse(
        total_count=total_count,
        items=[blog_orm_to_blog_response(blog) for blog in blogs]
    )