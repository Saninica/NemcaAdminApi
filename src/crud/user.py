from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.base import CRUDBase

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    async def get_user_by_username(self, db: AsyncSession, username: str):
        return await self.get_by_field(db, field_name="username", value=username)


    async def get_user_by_email(self, db: AsyncSession, email: str):
        return await self.get_by_field(db, field_name="email", value=email)


crud_user = CRUDUser(User)