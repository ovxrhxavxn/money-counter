from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from pathlib import Path

from .schemas import CVModelEnum, TaskSchema
from tasks import TasksSet
from database.database import SQLAlchemyDBHelper
from database.crud import SQLAlchemyCRUD
from utils import UtilsMethod


class CVAPI:

    __ROUTER = APIRouter(

        prefix='/cv',
        tags=['CV Model']
    )

    @property
    def router(self):
        return self.__ROUTER

    @staticmethod
    @__ROUTER.post(f'/{CVModelEnum.YOLO8S}', status_code=202)
    async def use_yolo8s(user_name: str, image: UploadFile, session: AsyncSession = Depends(SQLAlchemyDBHelper().get_async_session)):

        crud = SQLAlchemyCRUD(session)

        await crud.add_task(TaskSchema(result_path=None, msg_id=None))

        last_task = await crud.get_last_task()

        try:

            await crud.get_user(user_name)

        except IndexError:

            await crud.delete_task(last_task.id)

            raise HTTPException(404, detail='The user doesn`t exist')
        
        
        except Exception:

            await crud.delete_task(last_task.id)
        

        else:

            msg = TasksSet.use_yolo8s.send(user_name, last_task.id, await image.read())

            await crud.update_task_msg_id(last_task.id, msg.message_id)

            return {'task_id' : msg.message_id}
        

    @staticmethod
    @__ROUTER.post(f'/{CVModelEnum.YOLO8M}', status_code=202)
    async def use_yolo8m(user_name: str, image: UploadFile, session: AsyncSession = Depends(SQLAlchemyDBHelper().get_async_session)):

        crud = SQLAlchemyCRUD(session)

        cv_model_id = await crud.get_cv_model_id(CVModelEnum.YOLO8M)

        await crud.add_task(TaskSchema(cv_model_id=cv_model_id,result_path=None, msg_id=None))

        last_task = await crud.get_last_task()

        try:

            await crud.get_user(user_name)

            path = Path(f'database\\images\\{last_task.id}.jpeg').resolve()

            UtilsMethod().save_image(path, image.file.read())

            msg = TasksSet.use_yolo8m.send(user_name, last_task.id, str(path))

            await crud.update_task_msg_id(last_task.id, msg.message_id)

        except IndexError:

            await crud.delete_task(last_task.id)

            raise HTTPException(404, detail='The user doesn`t exist')
        
        except Exception:

            await crud.delete_task(last_task.id)
        
        else:

            return {'task_id' : msg.message_id}


    @staticmethod
    @__ROUTER.post(f'/{CVModelEnum.YOLO8N}', status_code=202)
    async def use_yolo8n(user_name: str, image: UploadFile, session: AsyncSession = Depends(SQLAlchemyDBHelper().get_async_session)):

        try:

            crud = SQLAlchemyCRUD(session)

            await crud.add_task(TaskSchema(result_path=None, msg_id=None))

            last_task = await crud.get_last_task()

            await crud.get_user(user_name)

            msg = TasksSet.use_yolo8n.send(user_name, last_task.id, await image.read())

            await crud.update_task_msg_id(last_task.id, msg.message_id)

        except IndexError:

            await crud.delete_task(last_task.id)

            raise HTTPException(404, detail='The user doesn`t exist')

        except Exception:

            await crud.delete_task(last_task.id)

        
        else:

            return {'task_id' : msg.message_id}

    @staticmethod
    @__ROUTER.get('/tasks/{task_id}')
    async def get_task_result(task_id: str, session: AsyncSession = Depends(SQLAlchemyDBHelper().get_async_session)):

        task = await SQLAlchemyCRUD(session).get_task_by_msg_id(task_id)

        if task.result_path is None:
        
            raise HTTPException(102, detail='The task is in processing')
        

        return str(UtilsMethod().read_image(Path(task.result_path).resolve()))