from pydantic import BaseModel, Field
from typing import List, Optional

# --------- Blog Schemas ---------
class BlogBase(BaseModel):
    title: str
    body: str

class BlogCreate(BlogBase):
    pass

class Blog(BlogBase):
    id: str = Field(..., alias="_id")
    creator_id: str

class ShowBlog(BlogBase):
    id: str = Field(..., alias="_id")
    creator: Optional["ShowUser"]

# --------- User Schemas ---------
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str = Field(..., alias="_id")

class ShowUser(UserBase):
    id: str = Field(..., alias="_id")
    blogs: List[Blog] = []

# --------- Auth Schemas ---------
class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Fix forward references
ShowBlog.update_forward_refs()
