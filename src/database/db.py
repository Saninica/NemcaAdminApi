from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.core.config import settings


engine = create_async_engine(
    settings.DATABASE_URI,
    echo=True,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URI else {}
)


async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def get_db():
    async with async_session() as session:
        yield session