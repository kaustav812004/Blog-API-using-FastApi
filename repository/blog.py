from database import blog_collection
from schemas import Blog
from bson import ObjectId

async def get_all():
    cursor = blog_collection.find()
    blogs = await cursor.to_list(length=100)
    for blog in blogs:
        blog["id"] = str(blog["_id"])
        del blog["_id"]
    return blogs

async def create(blog: Blog):
    result = await blog_collection.insert_one(blog.dict())
    return {"id": str(result.inserted_id), "msg": "Blog Created"}

async def show(id: str):
    blog = await blog_collection.find_one({"_id": ObjectId(id)})
    if blog:
        blog["id"] = str(blog["_id"])
        del blog["_id"]
    return blog

async def update(id: str, blog: Blog):
    await blog_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": blog.dict()}
    )
    return {"msg": "Blog updated"}

async def destroy(id: str):
    await blog_collection.delete_one({"_id": ObjectId(id)})
    return {"msg": "Blog Deleted"}