from fastapi.routing import APIRouter
from models.blog import BlogListResponse, Blog, BlogResponse, CreateBlog, EditBlog
from utils.blog_utils import blog_orm_to_blog_response, bulk_blog_orm_to_blog_response


blog_router = APIRouter(prefix='/blogs', tags=['Blogs'])

@blog_router.get('/', response_model=BlogListResponse)
async def get_blogs(page: int = 1, per_page: int = 10):
    blogs_query = Blog.all()
    count = await blogs_query.count()
    blogs = await blogs_query.offset((page - 1) * per_page).limit(per_page)
    return bulk_blog_orm_to_blog_response(blogs, count)

@blog_router.get('/{id}/', response_model=BlogResponse)
async def get_blog(id: int):
    blog = await Blog.get(id=id)
    return blog_orm_to_blog_response(blog)


@blog_router.post('/', response_model=BlogResponse)
async def create_blog(blog: CreateBlog):
    update_data = blog.model_dump()
    if 'keywords' in update_data:
        if len(update_data['keywords']) == 0:
            update_data['keywords'] = None
        else:
            update_data['keywords'] = '|'.join(update_data['keywords'])
    b = await Blog.create(**update_data)
    await b.save()
    return blog_orm_to_blog_response(b)

@blog_router.put('/{id}')
async def update_blog(id: int, blog: EditBlog):
    b = await Blog.get(id=id)
    blog_as_dict = blog.model_dump()
    update_data = {k: v for k, v in blog_as_dict.items() if v is not None}
    if not update_data:
        return
    if 'keywords' in update_data:
        if len(update_data['keywords']) == 0:
            update_data['keywords'] = None
        else:
            update_data['keywords'] = '|'.join(update_data['keywords'])
    await b.update_from_dict(update_data)
    await b.save()

@blog_router.delete('/{id}')
async def remove_blog(id: int):
    blog = await Blog.get(id=id)
    await blog.delete()