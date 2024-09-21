from pathlib import Path
from io import BytesIO
from typing import AsyncGenerator

from fastapi import UploadFile
from PIL.Image import Image

from database.repositories import (

    AbstractCVModelsRepository,
    AbstractTasksRepository,
    AbstractUserRepository
)
from .schemas import TaskSchema, CVModelEnum, TaskHistorySchema
from background_tasks.dramatiq.tasks  import use_cv_model
from cv_models.cv_processing.yolo8model import (

    YOLO8Model,
    YOLO8N,
    YOLO8S,
    YOLO8M
)


class CVModelsService:

    def __init__(
            
            self, 
            cv_model_repo: type[AbstractCVModelsRepository], 
            task_repo: type[AbstractTasksRepository], 
            user_repo: type[AbstractUserRepository]
            
            ):

        self._cv_model_repo = cv_model_repo()
        self._task_repo = task_repo()
        self._user_repo = user_repo()


    async def _use_model(self, user_name: str, cv_model: YOLO8Model, image: bytes) -> AsyncGenerator:

        cv_model_id = await self._cv_model_repo.get_id(cv_model.name)

        await self._task_repo.add(TaskSchema(cv_model_id=cv_model_id))

        last_task = await self._task_repo.get_last()

        try:

            await self._user_repo.get(user_name)

            path = Path(f'database/images/{last_task.id}.jpeg').resolve()

            bytes_io = BytesIO(image)

            

            msg = use_cv_model.send(cv_model, image)

            await self._task_repo.update_msg_id(last_task.id, msg.message_id)

            yield {'task_id' : msg.message_id}

            await self._task_repo.update_result(

                    msg.msg_id, 
                    str(Path(f'database/images/processed/{last_task.id}Result.jpeg'))
                    
                    )

            await self._task_repo.update_result_sum(last_task.id, msg.get_result()[0])

            cv_model_from_db = await self._cv_model_repo.get(cv_model.name)

            await self._user_repo.subtract_from_token_amount(user_name, cv_model_from_db.cost)

            user_id = await self._user_repo.get_id(user_name)

            await self._task_repo.add(TaskHistorySchema(

                user_id=user_id,
                task_id=last_task.id
            ))

        except IndexError:

            await self._task_repo.delete(last_task.id)

            raise
        
        except Exception:

            await self._task_repo.delete(last_task.id)
    


    async def use_yolo8s(self, user_name: str, image: UploadFile):
        
        await self._use_model(user_name, YOLO8S(), image.file.read())


    async def use_yolo8m(self, user_name: str, image: UploadFile):

       yield await self._use_model(user_name, YOLO8M(), image.file.read())


    async def use_yolo8n(self, user_name: str, image: UploadFile):

       yield await self._use_model(user_name, YOLO8N(), image.file.read())
    

    async def get(self, name: str):

        return await self._cv_model_repo.get(name)
    
    
    async def change_cost(self, name: str, new_value: int):

        await self._cv_model_repo.change_cost(name, new_value)


class TasksService:

    def __init__(self, task_repo: type[AbstractTasksRepository]):

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