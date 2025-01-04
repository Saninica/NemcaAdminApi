from src.models.user import User
from src.schemas.auth import Token
from src.schemas.user import UserCreate, UserRead
from src.crud import user as crud_user
from src.auth.jwt import create_access_token
from src.dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from src.models.user import User
from src.schemas.auth import Token
from src.schemas.user import UserCreate, UserRead
from src.auth.jwt import create_access_token
from src.dependencies import get_db, get_current_user
from passlib.context import CryptContext
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.user import crud_user


router = APIRouter()

@router.post("/auth/register/", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Kullanıcı adı zaten kullanılıyor.")
    db_user = await crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email zaten kullanılıyor.")
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")      
    user.hashed_password = pwd_context.hash(user.hashed_password)

    created_user = await crud_user.create(db=db, obj_in=user)

    return created_user

@router.post("/auth/login/", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud_user.get_user_by_username(db, username=form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Kullanıcı adı veya şifre yanlış.")

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    if not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Kullanıcı adı veya şifre yanlış.")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user": user}

@router.get("/auth/", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user