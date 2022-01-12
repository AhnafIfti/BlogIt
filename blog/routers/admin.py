from fastapi import APIRouter
from fastapi import status, HTTPException, File, UploadFile
from fastapi import FastAPI, Form, Depends
from sqlalchemy.util.deprecations import deprecated
from starlette.routing import request_response
from .. import models, database, hashing, oauth2, schemas
from ..database import engine
from sqlalchemy.orm import Session
from blog.oauth2 import get_current_user
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
    prefix = "/admin",
    tags=["Admin"]
)

# Make Admin
@router.put('/promote/{user_id}', status_code=status.HTTP_200_OK)
def update_admin(user_id: int, db: Session = Depends(database.get_db), admin_acc: bool = Form(...), current_user: schemas.User = Depends(oauth2.get_current_user)):
    edit_admin = db.query(models.User).filter(models.User.id == user_id)
    if not edit_admin.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with the id {user_id} is not available')
    edit_admin.update({'admin_acc': admin_acc})
    db.commit()
    return 'Updated Successfully'


# Delete User
@router.delete('/delete_user/{user_id}', status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    del_users = db.query(models.User).filter(models.User.id == user_id)
    if not del_users.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {user_id} is not available')
    del_users.delete(synchronize_session=False)
    db.commit()
    return 'deleted successfully'
