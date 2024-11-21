from fastapi.routing import APIRouter
from fastapi import status
from models.blog import BlogListResponse, Blog, BlogResponse, CreateBlog, EditBlog


blog_router = APIRouter(prefix='/blogs', tags=['Blogs'])

@blog_router.get('/', response_model=BlogListResponse)
async def get_blogs(page: int = 1, per_page: int = 10):
    blogs_query = Blog.all()
    count = await blogs_query.count()
    blogs = await blogs_query
    return BlogListResponse(total_count=count, items=blogs)

@blog_router.get('/{id}/', response_model=BlogResponse)
async def get_blog(id: int):
    blog = await Blog.get(id=id)
    return blog


@blog_router.post('/', response_model=BlogListResponse)
async def create_blog(blog: CreateBlog):
    b = await Blog.create(**blog.model_dump())
    await b.save()
    return b

@blog_router.put('/{id}')
async def update_blog(id: int, blog: EditBlog):
    b = await Blog.get(id=id)
    blog_as_dict = blog.model_dump()
    update_data = {k: v for k, v in blog_as_dict.items() if v is not None}
    if not update_data:
        return
    await b.update_from_dict(update_data)
    await b.save()

@blog_router.delete('/{id}')
async def remove_blog(id: int):
    blog = await Blog.get(id=id)
    await blog.delete()