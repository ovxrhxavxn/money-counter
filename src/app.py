import os

from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from pathlib import Path

from database.database import SQLAlchemyDBHelper
from database.crud import SQLAlchemyCRUD
from cv_models.schemas import CVModelEnum, CVModelSchema


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


    async def __create_and_fill_tables(self):
    
        if not os.path.exists(Path('database\\app.db')):

            db_helper = SQLAlchemyDBHelper()

            await db_helper.create_tables()

            async_generator = db_helper.get_async_session()

            session = await async_generator.__anext__()

            await SQLAlchemyCRUD(session).fill_cv_model_table()


    @asynccontextmanager
    async def lifespan(self, app: FastAPI):

        await self.__create_and_fill_tables()

        yield