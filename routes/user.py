from fastapi import APIRouter, status, Depends
from schemas import UserCreate, ShowUser
from repository import user
from oauth2 import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(request: UserCreate):
    return await user.create(request)

@router.get("/{id}", response_model=ShowUser)
async def get_user(id: str, current_user: dict = Depends(get_current_user)):
    return await user.show(id)
