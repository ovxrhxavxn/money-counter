from pathlib import Path
from PIL import Image

import dramatiq

from database.repositories import (

    AbstractCVModelRepository,
    AbstractTaskRepository,
    AbstractUserRepository,
    AbstractImageRepository
)
from .schemas import TaskSchema, TaskId, TaskHistorySchema
from cv_models.core.yolo8model import (

    YOLO8Model,
    YOLO8N,
    YOLO8S,
    YOLO8M
)
from images.schemas import ImageSchema


class CVModelsService:

    def __init__(
            
            self, 
            cv_model_repo: type[AbstractCVModelRepository], 
            task_repo: type[AbstractTaskRepository], 
            user_repo: type[AbstractUserRepository],
            image_repo: type[AbstractImageRepository]
            
            ):

        self._cv_model_repo = cv_model_repo()
        self._task_repo = task_repo()
        self._user_repo = user_repo()
        self._image_repo = image_repo()


    @dramatiq.actor
    @dramatiq.asyncio.async_to_sync
    async def _use_cv_model(

            self, 
            cv_model: YOLO8Model, 
            image: bytes, 
            task_id: int, 
            user_name: str
        
        ):

        sum, _, _ = cv_model.use(image)

        task: TaskId = await self._task_repo.get(task_id)

        await self._task_repo.update_result(task.msg_id, str(Path(f'images/processed/{task_id}Result.jpeg')))

        await self._task_repo.update_result_sum(task_id, sum)

        await self._user_repo.subtract_from_token_amount(user_name, cv_model.cost)

        user_id = await self._user_repo.get_id(user_name)

        await self._task_repo.add(TaskHistorySchema(

                user_id=user_id,
                task_id=task_id
        
            ).model_dump()
        )


    async def _set_cv_model_task(self, user_name: str, cv_model: YOLO8Model, image: bytes):

        cv_model_id = await self._cv_model_repo.get_id(cv_model.name)

        await self._task_repo.add(

            TaskSchema(

                cv_model_id=cv_model_id, 
                msg_id=None, 
                result_sum=None

            ).model_dump()
        )
        
        last_task = await self._task_repo.get_last()

        try:

            await self._user_repo.get(user_name)

            path = str(Path(f'images/{last_task.id}.jpeg'))

            Image.open(path).save(image)

            ImageSchema(

                path = path

            ).model_dump()

            msg = self._use_cv_model.send(self, cv_model, image, last_task.id, user_name)

            await self._task_repo.update_msg_id(last_task.id, msg.message_id)

        except IndexError:

            await self._task_repo.delete(last_task.id)

            raise
        
        except Exception:

            await self._task_repo.delete(last_task.id)

            raise
        
        else:

            return {'task_id' : msg.message_id}
        
    
    async def use_yolo8s(self, user_name: str, image: bytes):
        return await self._set_cv_model_task(user_name, YOLO8S(), image)


    async def use_yolo8m(self, user_name: str, image: bytes):
       return await self._set_cv_model_task(user_name, YOLO8M(), image)


    async def use_yolo8n(self, user_name: str, image: bytes):
       return await self._set_cv_model_task(user_name, YOLO8N(), image)
    

    async def get(self, name: str):
        return await self._cv_model_repo.get(name)
    
    
    async def change_cost(self, name: str, new_value: int):
        await self._cv_model_repo.change_cost(name, new_value)


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