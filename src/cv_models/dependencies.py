from .services import CVModelsService, TasksService
from .repositories import CVModelRepository, TaskRepository
from users.repositories import UserRepository


def get_cv_models_service():

    return CVModelsService(

        CVModelRepository,
        TaskRepository,
        UserRepository
    )


def get_tasks_service():

    return TasksService(TaskRepository)