from os import name
from typing import Optional
from pydantic import BaseModel

class Blog(BaseModel):
    pass


class User(BaseModel):
    name: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

    