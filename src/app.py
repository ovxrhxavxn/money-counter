from contextlib import asynccontextmanager

from fastapi import (

    FastAPI
)

from database.database import SQLAlchemyDBHelper
from users.router import router as users_router
from cv_models.router import router as cv_models_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    await SQLAlchemyDBHelper().create_tables()

    yield


app = FastAPI(

    lifespan=lifespan,
    title='Money Counter',
    summary='Backend для проекта Money Counter',
    version='1.0.0'

    )

routers = [

    users_router,
    cv_models_router
]

for router in routers:
    app.include_router(router)