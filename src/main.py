from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.database import engine, Base
from src.models.user import User
from src.schemas.auth import Token
from src.schemas.user import UserCreate, UserRead
from src.crud import user as crud_user
from src.auth.jwt import create_access_token
from src.dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from datetime import timedelta

# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/auth/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Kullanıcı adı zaten kullanılıyor.")
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email zaten kullanılıyor.")
    created_user = crud_user.create_user(db=db, user=user)
    return created_user

@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_user.get_user_by_username(db, username=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Kullanıcı adı veya şifre yanlış.")
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Kullanıcı adı veya şifre yanlış.")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user": user}

@app.get("/users/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
