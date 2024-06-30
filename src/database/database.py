from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator


class Base(DeclarativeBase): pass

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///database/app.db"
 
# создание движка
engine = create_async_engine(
    url=SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def create_tables():
       
       async with engine.begin() as conn:
           await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:

    async with async_session_maker() as session:
        yield session