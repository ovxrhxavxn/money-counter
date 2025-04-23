from pathlib import Path
import io
from PIL import Image

import dramatiq
from sqlalchemy.exc import NoResultFound
from fastapi.exceptions import HTTPException

from .services import (

    CVModelsService,
    TasksService
)
from users.services import UsersService
from .core.yolo8model import YOLO8Model
from .schemas import TaskSchema, TaskId, TaskHistorySchema
from cv_models.core.yolo8model import (

    YOLO8Model,
    YOLO8N,
    YOLO8S,
    YOLO8M
)
from images.schemas import ImageSchema


class UseCVModelUseCase:

    def __init__(
            
            self,      
            cv_model_service: CVModelsService,
            task_service: TasksService,
            user_service: UsersService
            
            ):
        
        self._task_service = task_service
        self._cv_model_service = cv_model_service
        self._user_service = user_service
        

    @dramatiq.actor
    @dramatiq.asyncio.async_to_sync
    async def _set_cv_model_result(

            self, 
            cv_model: type[YOLO8Model], 
            image: str,
            task_id: int, 
            user_name: str
        
        ):

        model_result = cv_model().use(bytes(image))

        path = Path(f'images/processed/{task_id}Result.jpeg')

        task: TaskId = await self._task_service.get(task_id)

        Image.open(io.BytesIO(model_result.img_byte_main)).save(path, format='jpeg')

        await self._task_service.update_result(task.msg_id, str(path))

        await self._task_service.update_result_sum(task_id, model_result.message_sum)

        await self._user_service.subtract_from_token_amount(user_name, 10)

        user_id = await self._user_service.get_id(user_name)

        await self._task_service.add(TaskHistorySchema(

                user_id=user_id,
                task_id=task_id
        
            ).model_dump()
        )


    async def _set_cv_model_task(self, user_name: str, cv_model: type[YOLO8Model], image: bytes):

        cv_model_id = await self._cv_model_service.get_id(cv_model.name)

        await self._task_service.add(

            TaskSchema(

                cv_model_id=cv_model_id, 
                msg_id=None, 
                image_id=None,
                result_sum=None

            ).model_dump()
        )
        
        last_task = await self._task_service.get_last()

        try:

            await self._user_service.get(user_name)

        except NoResultFound:

            await self._task_service.delete(last_task.id)

            raise HTTPException(404, detail='The user doesn`t exist')
        
        except Exception:

            await self._task_service.delete(last_task.id)

            raise HTTPException(404, detail='The user doesn`t exist')
        
        else:

            path = str(Path(f'images/{last_task.id}.jpeg'))

            Image.open(io.BytesIO(image)).save(path, format='jpeg')

            ImageSchema(

                path = path

            ).model_dump()

            msg = self._set_cv_model_result.send(cv_model, str(image), last_task.id, user_name)
            
            await self._task_service.update_msg_id(last_task.id, msg.message_id)

            return {"task_id" : msg.message_id}
     

    async def use_yolo8s(self, user_name: str, image: bytes):
        return await self._set_cv_model_task(user_name, YOLO8S, image)


    async def use_yolo8m(self, user_name: str, image: bytes):
        return await self._set_cv_model_task(user_name, YOLO8M, image)


    async def use_yolo8n(self, user_name: str, image: bytes):
        return await self._set_cv_model_task(user_name, YOLO8N, image)