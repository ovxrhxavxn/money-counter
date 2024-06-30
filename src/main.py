from fastapi import FastAPI
from contextlib import asynccontextmanager

from cv_models.router import router as cv_router
from users.router import router as users_router
from database.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    await create_tables()

    yield   

app = FastAPI(
    lifespan=lifespan,
    title='Money Counter',
    summary='Backend для проекта Money Counter',
    version='1.0.0'
)

routers = [

    cv_router,
    users_router
]

for router in routers:
    app.include_router(router)