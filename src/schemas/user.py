from pydantic import BaseModel, EmailStr
from typing import Optional
from src.schemas.website import WebsiteSchema

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    hashed_password: str

class UserRead(UserBase):
    id: int
    is_superuser: bool
    websites: list[WebsiteSchema] = []

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: str

    class Config:
        from_attributes = True