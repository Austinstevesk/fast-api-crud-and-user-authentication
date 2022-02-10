from pydantic import BaseModel
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
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True


    #This allows the app to work with thw data even if it is not a dictionary
    class Config:
        orm_mode = True