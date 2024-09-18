import io
from pathlib import Path

from fastapi import UploadFile
from fastapi.exceptions import HTTPException
from PIL.Image import Image

from .repositories import CVModelRepository, TaskRepository
from users.repositories import UserRepository
from .schemas import TaskSchema, CVModelEnum

class CVModelsService:

    def __init__(
            
            self, 
            cv_model_repo: type[CVModelRepository], 
            task_repo: type[TaskRepository], 
            user_repo: type[UserRepository]
            
            ):

        self._cv_model_repo = cv_model_repo()
        self._task_repo = task_repo()
        self._user_repo = user_repo()


    async def _use(self, user_name: str, cv_model_name: CVModelEnum, image: UploadFile) -> dict | None:

        cv_model_id = await self._cv_model_repo.get_id(cv_model_name)

        await self._task_repo.add(TaskSchema(cv_model_id=cv_model_id))

        last_task = await self._task_repo.get_last()

        try:

            await self._user_repo.get_by_name(user_name)

            path = Path(f'database/images/{last_task.id}.jpeg').resolve()

            Image().save(path, image.file.read())

            msg = "TasksSet.use_yolo8s.send(user_name, last_task.id, str(path))"

            await self._task_repo.update_msg_id(last_task.id, msg.message_id)

        except IndexError:

            await self._task_repo.delete(last_task.id)

            raise HTTPException(404, detail='The user doesn`t exist')
        
        except Exception:

            await self._task_repo.delete(last_task.id)
        
        else:

            return {'task_id' : msg.message_id}


    async def use_yolo8s(self, user_name: str, image: UploadFile):

        return await self._use(user_name, CVModelEnum.YOLO8S, image)


    async def use_yolo8m(self, user_name: str, image: UploadFile):

        return await self._use(user_name, CVModelEnum.YOLO8M, image)


    async def use_yolo8n(self, user_name: str, image: UploadFile):

       return await self._use(user_name, CVModelEnum.YOLO8N, image)
    

    async def get(self, name: str):

        return await self._cv_model_repo.get(name)
    
    
    async def change_cost(self, name: str, new_value: int):

        await self._cv_model_repo.change_cost(name, new_value)