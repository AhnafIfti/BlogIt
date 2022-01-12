from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from .. import models, database, schemas, oauth2, token
from sqlalchemy.orm import Session
from pathlib import Path

router = APIRouter(
    tags=["Admin"]
)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.get("/download/{blog_id}")
async def download_file(blog_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    dfilename = str(blog.filename)

    BASE_DIR = Path(__file__).resolve().parent
    dpathfilename = f'static/images/'+dfilename
    file_path = str(BASE_DIR.joinpath(dpathfilename))
    
    fileD = FileResponse(path=file_path, filename=dfilename, media_type='application/octet-stream')
    
    access_token = create_access_token(data={"filename": dfilename})
    
    return fileD

