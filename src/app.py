from contextlib import asynccontextmanager

from fastapi import (

    FastAPI
)

from users.router import router as users_router
from cv_models.router import router as cv_models_router
from database.orm.sqlalchemy.stuff import create_tables
from cv_models.dependencies import get_cv_models_service


@asynccontextmanager
async def lifespan(app: FastAPI):

    await create_tables()
    # await get_cv_models_service().fill_table_once()

    yield


app = FastAPI(

    lifespan=lifespan,
    title='Money Counter',
    summary='Backend для проекта Money Counter',
    version='0.1.0'

    )

routers = [

    users_router,
    cv_models_router
]

for router in routers:
    app.include_router(router)