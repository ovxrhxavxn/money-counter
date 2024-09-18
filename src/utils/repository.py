from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    async def add(self):
        pass

    @abstractmethod
    async def get(self):
        pass

    @abstractmethod
    async def delete(self):
        pass