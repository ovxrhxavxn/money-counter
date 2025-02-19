from pathlib import Path

import dramatiq
from dramatiq import Message
from dramatiq.results.errors import ResultMissing

from database.repositories import (

    AbstractCVModelRepository,
    AbstractTaskRepository,
    AbstractUserRepository
)
from .schemas import TaskSchema, TaskHistorySchema
from background_tasks.tasks  import use_cv_model
from cv_models.core.yolo8model import (

    YOLO8Model,
    YOLO8N,
    YOLO8S,
    YOLO8M
)


class CVModelsService:

    def __init__(
            
            self, 
            cv_model_repo: type[AbstractCVModelRepository], 
            task_repo: type[AbstractTaskRepository], 
            user_repo: type[AbstractUserRepository]
            
            ):

        self._cv_model_repo = cv_model_repo()
        self._task_repo = task_repo()
        self._user_repo = user_repo()


    async def _use_model(self, cv_model: YOLO8Model, image: bytes):

        # TODO: Реализовать бизнес-логику использования модели

        msg = use_cv_model.send(cv_model, image)
        
    
    async def use_yolo8s(self, user_name: str, image: bytes):
        return await self._use_model(user_name, YOLO8S(), image)


    async def use_yolo8m(self, user_name: str, image: bytes):
       return await self._use_model(user_name, YOLO8M(), image)


    async def use_yolo8n(self, user_name: str, image: bytes):
       return await self._use_model(user_name, YOLO8N(), image)
    

    async def get(self, name: str):
        return await self._cv_model_repo.get(name)
    
    
    async def change_cost(self, name: str, new_value: int):
        await self._cv_model_repo.change_cost(name, new_value)


    async def fill_table(self):
        await self._cv_model_repo.fill_table()


class TasksService:

    def __init__(self, task_repo: type[AbstractTaskRepository]):
        self._task_repo = task_repo()


    async def get_by_msg_id(self, msg_id: str):
        return await self._task_repo.get_by_msg_id(msg_id)
    

    async def update_result(self, msg_id: str, new_result: str):
        await self._task_repo.update_result(msg_id, new_result)


    async def get_last(self):
        return await self._task_repo.get_last()
    

    async def update_msg_id(self, new_msg_id: str):
        await self._task_repo.update_msg_id(new_msg_id)

    
    async def update_result_sum(self, id: int, new_sum: int):
        await self._task_repo.update_result_sum(id, new_sum)


    async def check_task_result(self, msg_id: str):
        task = await self._task_repo.get_by_msg_id(msg_id)

        if not task.image_id:
            raise ValueError("Task result is None")
        
        return task