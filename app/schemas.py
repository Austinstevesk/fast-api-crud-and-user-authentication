from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


#Create different schemas to handle different cases
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  
    


class CreatePost(PostBase):
    pass #This is because it has all the fields from PostBase
    
 

class UpdatePost(PostBase):
    pass #Already has all properties from PostBase


#Response model - we don't want to send everything as the response
class PostResponse(PostBase):
    id: int
    created_at: datetime


    #This allows the app to work with the data even if it is not a dictionary
    #Because by default what will be the output is sqlalchemy model
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class CreateUserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]