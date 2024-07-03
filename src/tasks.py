import dramatiq

import dramatiq.asyncio
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO
from pathlib import Path

from database.crud import SQLAlchemyCRUD
from database.database import SQLAlchemyDBHelper
from cv_models.schemas import TaskSchema, TaskId
from cv_models.cv_processing.model import work_with_items
from utils import UtilsMethod


broker = RedisBroker(url='redis://localhost:6379')
broker.add_middleware(AsyncIO())
dramatiq.set_broker(broker)

class TasksSet:

    @dramatiq.actor
    @dramatiq.asyncio.async_to_sync
    @staticmethod
    async def use_yolo8s(user_name: str, task_id: int, image_path: Path):

        sql_crud = SQLAlchemyCRUD()
        
        # TODO: Реализация работы с моделью

        #sum, main_img, imgs_array = work_with_items(bytes(image))

        async_generator = SQLAlchemyDBHelper().get_async_session()

        session = await async_generator.__anext__()

        task: TaskId = await sql_crud.get_task_by_id(session, task_id)

        await sql_crud.update_task_result(session, task.msg_id, 'main_img')

        await sql_crud.update_user_token_amount(session, user_name, 5)


    @dramatiq.actor
    @dramatiq.asyncio.async_to_sync
    @staticmethod
    async def use_yolo8m(user_name: str, task_id: int, image_path: str):

        sql_crud = SQLAlchemyCRUD()

        utils_method = UtilsMethod()
        
        # TODO: Реализация работы с моделью

        image_bytes = utils_method.read_image(image_path)

        sum, main_img, imgs_array = work_with_items(task_id, image_bytes)

        async_generator = SQLAlchemyDBHelper().get_async_session()

        session = await async_generator.__anext__()

        task: TaskSchema = await sql_crud.get_task_by_id(session, task_id)

        await sql_crud.update_task_result(session, task.msg_id, str(Path(f'database\\images\\processed\\{task_id}Result.jpeg')))

        await sql_crud.update_user_token_amount(session, user_name, 10)


    @dramatiq.actor
    @dramatiq.asyncio.async_to_sync
    @staticmethod
    async def use_yolo8n(user_name: str, task_id: int, image: bytes):
        
        # TODO: Реализация работы с моделью

        async_generator = SQLAlchemyDBHelper().get_async_session()

        session = await async_generator.__anext__()

        task: TaskSchema = await SQLAlchemyCRUD().get_task_by_id(session, task_id)

        await SQLAlchemyCRUD().update_task_result(session, task.msg_id, 'new result from y8n')

        await SQLAlchemyCRUD().update_user_token_amount(session, user_name, 15)