from sqlalchemy import select, insert, delete

from utils.repository import AbstractRepository
from .stuff import async_session_maker


class SQLAlchemyRepository(AbstractRepository):

    model  = None

    async def add(self, data: dict):

        async with async_session_maker() as session:

            stmt = insert(self.model).values(**data)

            await session.execute(stmt)
            await session.commit()

    
    async def get(self, id: int):
        
        async with async_session_maker() as session:

            query = select(self.model).where(self.model.id == id)

            result = await session.execute(query)

            return result.scalar_one()
        

    async def delete(self, id: int):

        async with async_session_maker() as session:

            stmt = delete(self.model).where(self.model.id == id)

            await session.execute(stmt)
            await session.commit()