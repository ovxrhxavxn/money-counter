from fastapi import FastAPI

from .cv_models.router import router as cv_models_router


app = FastAPI()

app.include_router(cv_models_router)