from .services import CVModelsService, TasksService
from .repositories import CVModelRepository, TaskRepository
from .use_cases import UseCVModelUseCase
from users.dependencies import get_user_service


def get_cv_models_service() -> CVModelsService:
    return CVModelsService(

        CVModelRepository
    )


def get_tasks_service() -> TasksService:
    return TasksService(TaskRepository)


def get_cv_models_use_case() -> UseCVModelUseCase:
    return UseCVModelUseCase(

        get_cv_models_service(),
        get_tasks_service(),
        get_user_service()
    )