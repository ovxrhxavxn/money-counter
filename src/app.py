from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager

from database.database import SQLAlchemyDBHelper


class FastAPIAppWrapper:

    def __init__(self):

        self.__app = FastAPI(

            lifespan=self.lifespan,
            title='Money Counter',
            summary='Backend для проекта Money Counter',
            version='1.0.0'
        )

    @property
    def app(self):
        return self.__app
    

    def include_routers_to_app(self, routers: list[APIRouter]):

        for router in routers:
            self.__app.include_router(router)

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
    
        await SQLAlchemyDBHelper().create_tables()

        yield