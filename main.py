from typing import Optional
from fastapi import FastAPI

app = FastAPI()


@app.get('/blog/{blog_id}')
def create_blog(blog_id: int, limit: int = 10, published: bool = True, sort: Optional[str] = None):
    return {'data': f'Blog is created with title as {blog_id}'}
