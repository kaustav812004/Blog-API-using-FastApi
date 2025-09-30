from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth_token import verify_token
from database import user_collection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token_str: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token_str, credentials_exception)
    user = await user_collection.find_one({"email": token_data.email})
    if not user:
        raise credentials_exception
    user["_id"] = str(user["_id"])
    return user
