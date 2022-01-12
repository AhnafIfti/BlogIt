from fastapi import status, HTTPException, File, UploadFile
from fastapi import FastAPI, Form, Depends
from sqlalchemy.sql.functions import user
from sqlalchemy.util.deprecations import deprecated
from starlette.routing import request_response
from . import models, database, hashing
from .database import engine
from sqlalchemy.orm import Session

from blog import routers
'''For Template Purpose'''
from fastapi import Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
'''Photo Upload'''
import shutil
'''Static Files'''
from fastapi.staticfiles import StaticFiles
'''APIRouter'''
from .routers import admin, user, blog, authentication, downloadFile


app = FastAPI()

models.Base.metadata.create_all(engine)

'''Define Base Path'''
BASE_DIR = Path(__file__).resolve().parent
Template_dir = str(BASE_DIR.joinpath('htmldirectory'))

'''Define Static Path'''
static_dir = str(BASE_DIR.joinpath('routers/static/images'))
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(authentication.router)
app.include_router(admin.router)
app.include_router(user.router)
app.include_router(blog.router)
app.include_router(downloadFile.router)
