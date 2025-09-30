from database import user_collection
from hashing import Hash
from bson import ObjectId
from schemas import UserCreate
from fastapi import HTTPException, status


async def create(request: UserCreate):
    existing_user = await user_collection.find_one({"email": request.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if not isinstance(request.password, str):
        raise HTTPException(status_code=400, detail="Password must be a string")

    user_data = {
        "name": request.name,
        "email": request.email,
        "password": Hash.bcrypt(request.password[:72])  # truncate to 72 bytes
    }
    result = await user_collection.insert_one(user_data)
    user_data["_id"] = str(result.inserted_id)
    return user_data

async def show(id: str):
    try:
        user = await user_collection.find_one({"_id": ObjectId(id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid user id format")
    
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    
    user["_id"] = str(user["_id"])
    return user
