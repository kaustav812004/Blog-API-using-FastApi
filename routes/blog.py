# routes/blog.py
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from schemas import BlogCreate, ShowBlog, User
from repository import blog
from oauth2 import get_current_user

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)

# Get all blogs
@router.get('/', response_model=List[ShowBlog])
async def all(current_user: User = Depends(get_current_user)):
    blogs = await blog.get_all()
    return blogs

# Create a new blog
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ShowBlog)
async def create(request: BlogCreate, current_user: User = Depends(get_current_user)):
    new_blog = await blog.create(request, current_user.id)
    return new_blog

# Get a blog by ID
@router.get('/{id}', response_model=ShowBlog)
async def show(id: str, current_user: User = Depends(get_current_user)):
    blog_data = await blog.show(id)
    if not blog_data:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog_data

# Update a blog
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=ShowBlog)
async def update(id: str, request: BlogCreate, current_user: User = Depends(get_current_user)):
    updated_blog = await blog.update(id, request, current_user.id)
    if not updated_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return updated_blog

# Delete a blog
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id: str, current_user: User = Depends(get_current_user)):
    deleted = await blog.destroy(id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"msg": "Blog deleted"}
