from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.crud.user import crud_user
from src.auth.jwt import verify_access_token, blacklist_token
from src.models.user import User
from typing import Tuple


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Geçersiz kimlik dogrulama bilgileri.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    user = await crud_user.get(db, filters={"username": token_data.username}, load_relations=[User.websites])
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_user_with_token(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> Tuple[User, str]:
    """
    Get current user along with token data for operations that need access to token info (like logout)
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Geçersiz kimlik dogrulama bilgileri.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    user = await crud_user.get(db, filters={"username": token_data.username}, load_relations=[User.websites])
    if user is None:
        raise credentials_exception
    
    return user, token_data.jti
