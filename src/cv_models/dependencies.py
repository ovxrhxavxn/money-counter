from .services import CVModelsService, TasksService
from .repositories import CVModelRepository, TaskRepository
from users.repositories import UserRepository


def get_cv_models_service() -> CVModelsService:
    return CVModelsService(

        CVModelRepository,
        TaskRepository,
        UserRepository
    )


def get_tasks_service() -> TasksService:
    return TasksService(TaskRepository)