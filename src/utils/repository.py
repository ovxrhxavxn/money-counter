from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one(self):
        raise NotImplementedError()
    
    @abstractmethod
    async def find_all(self):
        raise NotImplementedError()
    

class SQLAlchemyRepository(AbstractRepository):

    model = None

    async def add_one(self):
        raise NotImplementedError()

    async def find_all(self):
        raise NotImplementedError()