from fastapi import APIRouter
from fastapi import status, HTTPException, File, UploadFile
from fastapi import FastAPI, Form, Depends
from sqlalchemy.util.deprecations import deprecated
from starlette.routing import request_response
from .. import models, database, hashing
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

router = APIRouter(
    prefix = "/user",
    tags=["User"]
)

# Create User
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(database.get_db)):
    new_user = models.User(name=name, email=email, password=hashing.Hash.bcrypt(password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return 'Created Successfully'

# Get All Users
@router.get('/', status_code=status.HTTP_200_OK)
def all_users(request: Request, db: Session = Depends(database.get_db)):
    all_users = db.query(models.User).all()
    if not all_users:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No blog is available')
        return templates.TemplateResponse("all_users.html", {"request": request, "no_users": "No user is available"})
    return templates.TemplateResponse("all_users.html", {"request": request, "all_users": all_users})


# Get User by User Id
@router.get('/{user_id}', status_code=status.HTTP_200_OK)
def user_uid(user_id: int, request: Request, db: Session = Depends(database.get_db)):
    users_uid = db.query(models.User).filter(models.User.id == user_id).first()
    # users_photo = db.query(models.FileUpload).filter(models.FileUpload.user_id == user_id).first()
    if not users_uid:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog is not available')
        return templates.TemplateResponse("user_uid.html", {"request": request, "no_users": "No user is available"})
    else:
        # return templates.TemplateResponse("user_uid.html", {"request": request, "users_uid": users_uid, "users_photo": users_photo})
        return templates.TemplateResponse("user_uid.html", {"request": request, "users_uid": users_uid})


# Edit User
@router.put('/update/{user_id}', status_code=status.HTTP_200_OK)
def update_user(user_id: int, db: Session = Depends(database.get_db), name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    edit_users = db.query(models.User).filter(models.User.id == user_id)
    if not edit_users.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with the id {user_id} is not available')
    edit_users.update({'name': name, 'email': email, 'password': hashing.Hash.bcrypt(password)})
    db.commit()
    return 'Updated Successfully'
