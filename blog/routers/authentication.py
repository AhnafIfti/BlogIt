from fastapi import APIRouter, status, HTTPException
from fastapi import Form, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..hashing import Hash
from blog.hashing import Hash
from .. import database, models
from sqlalchemy.orm import Session
from .. import token

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credential')
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credential')
    if user.admin_acc == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credential')

    access_token = token.create_access_token(data={"sub": user.email, "user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}
