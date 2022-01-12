from fastapi import APIRouter
from fastapi import status, HTTPException, File, UploadFile
from fastapi import FastAPI, Form, Depends
from sqlalchemy.util.deprecations import deprecated
from starlette.routing import request_response
from .. import models, database, hashing, oauth2, schemas
from ..database import engine
from sqlalchemy.orm import Session
'''For Template Purpose'''
from fastapi import Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
'''Photo Upload'''
import shutil
'''Static Files'''
from fastapi.staticfiles import StaticFiles

app = FastAPI()

models.Base.metadata.create_all(engine)

'''Define Base Path'''
BASE_DIR = Path(__file__).resolve().parent
Template_dir = str(BASE_DIR.joinpath('htmldirectory'))
templates = Jinja2Templates(directory=Template_dir)

'''Define Static Path'''
static_dir = str(BASE_DIR.joinpath('static/images'))
app.mount("/static", StaticFiles(directory=static_dir), name="static")

'''Fetch Path'''
fetch_dir = str(BASE_DIR.joinpath('routers/static/images'))

router = APIRouter(
    prefix = "/blog",
    tags=["Blog"]
)

# Create Blog
@router.post('/{user_id}', status_code=status.HTTP_201_CREATED)
def create_blog(user_id: int, file: UploadFile = File(...), title: str = Form(...), body: str = Form(...), db: Session = Depends(database.get_db)):

    file_location = static_dir+f"\{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_blog = models.Blog(title=title, body=body, filename=file.filename, user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return 'Created Successfully'


# Get All Blogs
@router.get('/', status_code=status.HTTP_200_OK)
def all_blogs(request: Request, db: Session = Depends(database.get_db)):
    all_blogs = db.query(models.Blog).all()
    if not all_blogs:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No blog is available')
        return templates.TemplateResponse("all_blogs.html", {"request": request, "no_blogs": "No blog is available"})
    return templates.TemplateResponse("all_blogs.html", {"request": request, "all_blogs": all_blogs})

# Get Blog by Blog Id
@router.get('/{blog_id}', status_code=status.HTTP_200_OK)
def blog_bid(blog_id: int, request: Request, db: Session = Depends(database.get_db)):
    blogs_bid = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    # users_photo = db.query(models.FileUpload).filter(models.FileUpload.blog_id == blog_id).first()
    if not blogs_bid:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog is not available')
        return templates.TemplateResponse("blog_bid.html", {"request": request, "no_blogs": "Blog is not available"})
    else:
        # return templates.TemplateResponse("blog_bid.html", {"request": request, "blogs_bid": blogs_bid, "users_photo": users_photo})
        return templates.TemplateResponse("blog_bid.html", {"request": request, "blogs_bid": blogs_bid})


# Get Blog by User Id
@router.get('/user/{user_id}', status_code=status.HTTP_200_OK)
def blog_uid(user_id: int, request: Request, db: Session = Depends(database.get_db)):
    blogs_uid = db.query(models.Blog).filter(models.Blog.user_id == user_id)
    if not blogs_uid:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog is not available')
        return templates.TemplateResponse("blog_uid.html", {"request": request, "no_blogs": "No blog is available for this user"})
    else:
        return templates.TemplateResponse("blog_uid.html", {"request": request, "blogs_uid": blogs_uid})


# Delete Blog
@router.delete('/delete/{blog_id}', status_code=status.HTTP_200_OK)
def delete_blog(blog_id: int, db: Session = Depends(database.get_db)):
    del_blogs = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not del_blogs.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {blog_id} is not available')
    del_blogs.delete(synchronize_session=False)
    db.commit()
    return 'deleted successfully'

# Edit Blog
@router.put('/update/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id: int, db: Session = Depends(database.get_db), title: str = Form(...), body: str = Form(...)):
    edit_blogs = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not edit_blogs.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {blog_id} is not available')
    edit_blogs.update({'title': title, 'body': body})
    db.commit()
    return 'Updated Successfully'

