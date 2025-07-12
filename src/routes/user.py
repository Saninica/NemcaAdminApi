from src.models.user import User
from src.schemas.auth import Token
from src.schemas.user import UserCreate, UserRead, UserRegister
from src.crud.user import crud_user
from src.auth.jwt import create_access_token, blacklist_token
from src.dependencies import get_db, get_current_user, get_current_user_with_token
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.post("/register/", response_model=UserRegister)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud_user.get(db, filters={"username": user.username}, load_relations=[User.websites])
    if db_user:
        raise HTTPException(status_code=400, detail="Kullanıcı adı zaten kullanılıyor.")

    db_user = await crud_user.get(db, filters={"email": user.email}, load_relations=[User.websites])
    if db_user:
        raise HTTPException(status_code=400, detail="Email zaten kullanılıyor.")
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")      
    # Hash the plaintext password received from client
    hashed_password = pwd_context.hash(user.password)
    
    # Create a new user dict with the hashed password
    user_data = user.dict()
    user_data["hashed_password"] = hashed_password
    del user_data["password"]  # Remove plaintext password

    created_user = await crud_user.create(db=db, obj_in=user_data)

    return created_user

@router.post("/login/", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud_user.get(db, filters={"username": form_data.username}, load_relations=[User.websites])

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
    
    websites_data = [{"id": website.id, "name": website.name} for website in user.websites]

    user_data = UserRead(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        websites=websites_data
    )

    return {"access_token": access_token, "token_type": "bearer", "user": user_data}

@router.post("/logout/")
async def logout(user_data: tuple = Depends(get_current_user_with_token)):
    """
    Logout endpoint that invalidates the current user's token
    """
    current_user, token_jti = user_data
    
    # Blacklist the token to prevent further use
    blacklist_token(token_jti)
    
    return {"message": "Successfully logged out"}

@router.get("/", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/website/", response_model=UserRead)
async def create_website(website_id: int,current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    data = await crud_user.create_website_for_user(db, website_id=website_id, user=current_user)
    return data