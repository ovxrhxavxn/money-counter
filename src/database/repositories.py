from abc import ABC, abstractmethod

from users.schemas import UserDate
from cv_models.schemas import TaskId, CVModelSchema


class AbstractUserRepository(ABC):

    @abstractmethod
    async def add(self):

        pass


    @abstractmethod
    async def get(self, name: str):

        pass
    

    @abstractmethod
    async def get_all(self) -> list[UserDate]:

        pass
    

    @abstractmethod
    async def subtract_from_token_amount(self, name: str, cost: int):

        pass


    @abstractmethod
    async def change_token_amount(self, name: str, new_value: int):

        pass


    @abstractmethod
    async def change_role(self, name: str, new_role: str):

        pass


    @abstractmethod
    async def get_id(self, user_name: str) -> int:

        pass
    

class AbstractTasksRepository(ABC):

    @abstractmethod
    async def add(self, schema: dict):

        pass


    @abstractmethod
    async def get(self, id: int) -> TaskId:

        pass


    @abstractmethod
    async def delete(self, id: int):

        pass


    @abstractmethod
    async def get_by_msg_id(self, msg_id: str):

        pass
    

    @abstractmethod
    async def update_result(self, msg_id: str, new_result: str):

        pass


    @abstractmethod
    async def get_last(self) -> TaskId:

        pass
    

    @abstractmethod
    async def update_msg_id(self, id: int, new_msg_id: str):

        pass


    @abstractmethod
    async def update_result_sum(self, id: int, new_sum: int):

        pass


class AbstractCVModelsRepository(ABC):

    @abstractmethod
    async def add(self):

        pass


    @abstractmethod
    async def get(self, name: str) -> CVModelSchema:

        pass
        

    @abstractmethod
    async def get_id(self, name: str) -> int:

        pass
        

    @abstractmethod
    async def change_cost(self, name: str, new_value: int):

        pass


class AbstractTaskHistoryRepository(ABC):

    @abstractmethod
    async def add(self, schema: dict):

        pass


    @abstractmethod
    async def get(self, name: str):

        pass
        

    @abstractmethod
    async def get_user_history(self, user_name: str):

        pass