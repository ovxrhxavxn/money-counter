from fastapi import FastAPI

from cv_models.router import router as cv_router
from users.router import router as users_router

app = FastAPI(

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