from .services import CVModelsService
from .repositories import CVModelRepository, TaskRepository
from users.repositories import UserRepository


def get_cv_models_service():

    return CVModelsService(

        CVModelRepository,
        TaskRepository,
        UserRepository
    )