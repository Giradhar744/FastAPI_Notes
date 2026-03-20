from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated
from datetime import datetime


class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True
    rating : Optional[int] = None

class CreatePost(PostBase):
    pass  # It simply inherits its parents property

class UserCreateResponse(BaseModel):
     id: int
     email : EmailStr
     created_at: datetime
     
     class Config:
        from_attributes = True

class PostResponse(PostBase):
     id: int
     created_at:  datetime
     owner_id: int
     owner:  UserCreateResponse
     
     class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: PostResponse
    Like_count: int

    class Config:
       from_attributes = True

class UserCreate(BaseModel):
        email: EmailStr
        password: str





class Userlogin(BaseModel):
     email : EmailStr
     password: str


class Token(BaseModel):
     access_token : str
     token_type : str


class Token_data(BaseModel):
     id : Optional[int] = None


class Vote(BaseModel):
     post_id: int
     like: Annotated[int, Field(ge= 0 , le=1, strict=True)]