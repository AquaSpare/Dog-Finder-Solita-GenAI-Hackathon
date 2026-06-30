import os

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://dogs:dogs@localhost:5432/dogs_db",
)

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with SessionLocal() as db:
        yield db
