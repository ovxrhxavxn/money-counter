from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager

from cv_models.router import CVAPIRouterWrapper
from users.router import UserAPIRouterWrapper
from database.database import SQLAlchemyDBHelper


class FastAPIWrapper:

    def __init__(self):


        self.__app = FastAPI(

            lifespan=self.lifespan,
            title='Money Counter',
            summary='Backend для проекта Money Counter',
            version='1.0.0'
        )

        self._routers: list[APIRouter] = [

            CVAPIRouterWrapper().router,
            UserAPIRouterWrapper().router
        ]

    @property
    def app(self):
        return self.__app
    
    @property
    def routers(self):
        return self._routers

    def include_routers(self):

        for router in self._routers:
            self.__app.include_router(router)

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):

        self.include_routers()
    
        await SQLAlchemyDBHelper().create_tables()

        yield