from pydantic import BaseModel
from typing import List

class Blog(BaseModel):
    title: str
    description: str | None = None
    body: str
    
class User(BaseModel):
    name: str
    email: str
    password: str
    
class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog]
    
    class Config:
        orm_mode = True
        
class ShowBlog(BaseModel):
    title: str
    description: str | None = None
    body: str
    writer: ShowUser
    
    class Config:
        orm_mode = True
        
class Login(BaseModel):
    email: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None