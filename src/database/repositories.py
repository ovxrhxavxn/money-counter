from typing import Protocol, Union, Any, TypeVar
from abc import ABC

from sqlalchemy import select, insert

from .orm.sqlalchemy.stuff import Base, async_session_maker
from users.schemas import UserDate
from cv_models.schemas import TaskId, CVModelSchema, TaskHistorySchema
from images.schemas import ImageSchema


Model = TypeVar('Model', bound=Base)


class SQLAlchemyRepository[Model](ABC):

    def __init__(self, model: type[Model]):
        self.model = model

    async def add(self, schema: dict) -> None:
        async with async_session_maker() as session:

            stmt = insert(self.model).values(schema)

            await session.execute(stmt)
            await session.commit()


    async def get_all(self) -> list[Model]:
        async with async_session_maker() as session:

            query = select(self.model)

            result = await session.execute(query)

            return result.all()


class AbstractUserRepository(Protocol):

    async def add(self, schema: dict):
        ...

    async def get(self, name: str) -> UserDate:
        ...

    async def get_all(self):
        ...
        
    async def subtract_from_token_amount(self, name: str, cost: int):
        ...

    async def change_token_amount(self, name: str, new_value: int):
        ...

    async def change_role(self, name: str, new_role: str):
        ...
        
    async def get_id(self, name: str) -> int:
        ...


class AbstractTaskRepository(Protocol):

    async def add(self, schema: dict):
        ...

    async def get(self, id: int) -> TaskId:
        ...

    async def get_all(self) -> list[TaskId]:
        ...

    async def delete(self, id: int):
        ...

    async def get_by_msg_id(self, msg_id: str) -> TaskId:
        ...
    
    async def update_result(self, msg_id: str, new_result: str):
        ...

    async def get_last(self) -> TaskId:
        ...
    
    async def update_msg_id(self, id: int, new_msg_id: str):
        ...

    async def update_result_sum(self, id: int, new_sum: int):
        ...


class AbstractCVModelRepository(Protocol):

    async def add(self, schema: Union[dict, Any]):
        ...

    async def get(self, name: str) -> CVModelSchema:
        ...

    async def get_all(self) -> list[CVModelSchema]:
        ...

    async def get_id(self, name: str) -> int:
        ...
        
    async def change_cost(self, name: str, new_value: int):
        ...

    async def fill_table(self):
        ...


class AbstractTaskHistoryRepository(Protocol):

    async def add(self, schema: dict):
        ...

    async def get(self, name: str) -> TaskHistorySchema:
        ...

    async def get_all(self) -> list[TaskHistorySchema]:
        ...
        
    async def get_user_history(self, user_name: str):
        ...


class AbstractImageRepository(Protocol):

    async def add(self, schema: dict):
        ...

    async def get_all(self) -> list[ImageSchema]:
        ...

    async def get(self, path: str) -> ImageSchema:
        ...