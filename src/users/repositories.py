from sqlalchemy import select, update

from database.orm.sqlalchemy.stuff import async_session_maker
from database.orm.sqlalchemy.models import User
from database.repositories import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[User]):

    def __init__(self):
        super().__init__(User)

    async def get(self, name: str):

        async with async_session_maker() as session:

            query = select(self.model).where(self.model.name == name)

            result = await session.execute(query)

            return result.scalar_one()
        

    async def get_id(self, name: str) -> int:
        async with async_session_maker() as session:

            query = select(self.model).where(self.model.name == name)

            result = await session.execute(query)

            return result.scalar_one().id
        

    async def subtract_from_token_amount(self, name: str, cost: int):

        user = await self.get(name)

        async with async_session_maker() as session:

            stmt = update(self.model).where(self.model.name == name).values(token_amount = user.token_amount - cost) 

            await session.execute(stmt)
            await session.commit()

    
    async def change_token_amount(self, name: str, new_value: int):

        async with async_session_maker() as session:

            stmt = update(self.model).where(self.model.name == name).values(token_amount = new_value) 

            await session.execute(stmt)
            await session.commit()


    async def change_role(self, name: str, new_role: str):

        async with async_session_maker() as session:
                
            stmt = update(self.model).where(self.model.name == name).values(role = new_role) 

            await session.execute(stmt)
            await session.commit()