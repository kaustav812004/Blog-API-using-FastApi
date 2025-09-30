from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from hashing import Hash
from database import user_collection
from auth_token import create_access_token

router = APIRouter(tags=['Authentication'])

@router.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends()):
    # Find user by email
    user = await user_collection.find_one({"email": request.username})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )
    
    if not Hash.verify(user["password"], request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect password"
        )

    # Generate JWT token
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
