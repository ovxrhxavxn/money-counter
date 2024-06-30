from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator


class Base(DeclarativeBase): pass

class SQLAlchemyDBHelper:

    __SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///database/app.db"

    def __init__(self):
        
        self._engine = create_async_engine(
             
            url=self.__SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )
 
        self._async_session_maker = sessionmaker(bind=self._engine, class_=AsyncSession, expire_on_commit=False)
        

    @property
    def db_url(self):
        return self.__SQLALCHEMY_DATABASE_URL
    

    async def create_tables(self):
       
       async with self._engine.begin() as conn:
           await conn.run_sync(Base.metadata.create_all)
           

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:

        async with self._async_session_maker() as session:
            yield session