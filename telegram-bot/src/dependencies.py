from .services import CVModelsService
from .repositories import FastAPIServiceRepository


def get_cv_model_service() -> CVModelsService:
    return CVModelsService(FastAPIServiceRepository)