from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.base import CRUDBase
from src.crud.website import crud_website
from fastapi import HTTPException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    async def create_website_for_user(self, db: AsyncSession, website_id: int, user: User):
        website = await crud_website.get(db, id=website_id)
        if not website:
            raise HTTPException(status_code=404, detail="Website not found")

        user.websites.append(website)

        await db.commit()
        await db.refresh(user)

        return user

crud_user = CRUDUser(User)