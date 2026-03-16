from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True
    rating : Optional[int] = None

class CreatePost(PostBase):
    pass  # It simply inherits its parents property

class PostResponse(PostBase):
     id: int
     created_at:  datetime
     owner_id: int
     
     class Config:
        from_attributes = True

class UserCreate(BaseModel):
        email: EmailStr
        password: str


class UserCreateResponse(BaseModel):
     id: int
     email : EmailStr
     created_at: datetime
     
     class Config:
        from_attributes = True


class Userlogin(BaseModel):
     email : EmailStr
     password: str


class Token(BaseModel):
     access_token : str
     token_type : str


class Token_data(BaseModel):
     id : Optional[int] = None