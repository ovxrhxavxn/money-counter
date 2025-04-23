from sqlalchemy import select, update, insert, delete

from database.orm.sqlalchemy.stuff import async_session_maker
from database.repositories import SQLAlchemyRepository
from database.orm.sqlalchemy.models import (

    Task,
    CVModelTable,
    TaskHistory
)
from .schemas import CVModelSchema
from .enums import CVModelEnum


class CVModelRepository(SQLAlchemyRepository[CVModelTable]):

    def __init__(self):
        super().__init__(CVModelTable)

    async def get(self, name: str):

        async with async_session_maker() as session:

            query = select(self.model).where(self.model.name == name)

            result = await session.execute(query)

            return result.scalar_one()
        

    async def change_cost(self, name: str, new_value: int):

        async with async_session_maker() as session:

            stmt = update(self.model).where(self.model.name == name).values(cost = new_value)

            await session.execute(stmt)
            await session.commit()


    async def get_id(self, name: str):

        async with async_session_maker() as session:

            query = select(self.model).where(self.model.name == name)

            result = await session.execute(query)

            return result.scalar_one().id
        

    async def fill_table(self):

        async with async_session_maker() as session:

            for i, model in enumerate(CVModelEnum):
                await session.execute(insert(self.model).values(CVModelSchema(name=model, cost=(i+1)*5).model_dump()))
                await session.commit()


class TaskRepository(SQLAlchemyRepository[Task]):

    def __init__(self):
        super().__init__(Task)
    
    async def get(self, id: int):

        async with async_session_maker() as session:
        
            query = select(self.model).where(self.model.id == id)

            result = await session.execute(query)

            task = result.scalar_one()

            return task
    

    async def get_by_msg_id(self, msg_id: str):

        async with async_session_maker() as session:
        
            query = select(self.model).where(self.model.msg_id == msg_id)

            result = await session.execute(query)

            task = result.scalar_one()

            return task
    

    async def update_result(self, msg_id: str, new_result: str):

        async with async_session_maker() as session:

            stmt = update(self.model).where(self.model.msg_id == msg_id).values(result_path=new_result)

            await session.execute(stmt)
            await session.commit()


    async def get_last(self) -> Task:

        async with async_session_maker() as session:

            query = select(self.model).order_by(self.model.id.desc())

            result = await session.execute(query)

            task = result.scalar_one()

            return task
    

    async def update_msg_id(self, id: int, new_msg_id: str):

        async with async_session_maker() as session:

            stmt = update(self.model).where(self.model.id == id).values(msg_id = new_msg_id)

            await session.execute(stmt)
            await session.commit()


    async def update_result_sum(self, id: int, new_sum: int):

        async with async_session_maker() as session:

            stmt = update(self.model).where(self.model.id == id).values(result_sum = new_sum)

            await session.execute(stmt)
            await session.commit()


    async def delete(self, id: int):

        async with async_session_maker() as session:

            stmt = delete(self.model).where(self.model.id == id)

            await session.execute(stmt)
            await session.commit()


class TaskHistoryRepository(SQLAlchemyRepository[TaskHistory]):

    def __init__(self):
        super().__init__(TaskHistory)

    async def get(self, name: str):

        async with async_session_maker() as session:

            query = select(self.model).where(self.model.name == name)

            result = await session.execute(query)

            model = result.scalar_one()

            return model
        

    async def add(self, schema: dict):

        async with async_session_maker() as session:

            stmt = insert(self.model).values(schema)

            await session.execute(stmt)
            await session.commit()


    async def get_user_history(self, user_name: str):
        pass 