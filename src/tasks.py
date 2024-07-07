import dramatiq
import dramatiq.asyncio

from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO
from pathlib import Path

from database.crud import SQLAlchemyCRUD
from database.database import SQLAlchemyDBHelper
from cv_models.schemas import TaskId, ImageHistorySchema, CVModelEnum
from cv_models.cv_processing.YOLO8Model import CVModel
from utils import UtilsMethod


broker = RedisBroker(url='redis://localhost:6379')
broker.add_middleware(AsyncIO())
dramatiq.set_broker(broker)

class TasksSet:

    @dramatiq.actor
    @dramatiq.asyncio.async_to_sync
    @staticmethod
    async def use_yolo8s(user_name: str, task_id: int, image_path: Path):
        
        utils_method = UtilsMethod()
        
        # TODO: Реализация работы с моделью

        image_bytes = utils_method.read_image(image_path)

        sum, _, _ = CVModel.Yolo8N_Work(task_id, image_bytes)

        async_generator = SQLAlchemyDBHelper().get_async_session()

        session = await async_generator.__anext__()

        crud = SQLAlchemyCRUD(session)

        task: TaskId = await crud.get_task_by_id(task_id)

        await crud.update_task_result(task.msg_id, str(Path(f'database\\images\\processed\\{task_id}Result.jpeg')))

        await crud.update_task_result_sum(task_id, sum)

        cv_model = await crud.get_cv_model(CVModelEnum.YOLO8M)

        await crud.subtract_from_user_token_amount(user_name, cv_model.cost)

        user_id = await crud.get_user_id(user_name)

        await crud.add_image_history(ImageHistorySchema(

            user_id=user_id,
            task_id=task_id
        ))


    @dramatiq.actor
    @dramatiq.asyncio.async_to_sync
    @staticmethod
    async def use_yolo8m(user_name: str, task_id: int, image_path: str):

        utils_method = UtilsMethod()
        
        # TODO: Реализация работы с моделью

        image_bytes = utils_method.read_image(image_path)

        sum, _, _ = CVModel.Yolo8N_Work(task_id, image_bytes)

        async_generator = SQLAlchemyDBHelper().get_async_session()

        session = await async_generator.__anext__()

        crud = SQLAlchemyCRUD(session)

        task: TaskId = await crud.get_task_by_id(task_id)

        await crud.update_task_result(task.msg_id, str(Path(f'database\\images\\processed\\{task_id}Result.jpeg')))

        await crud.update_task_result_sum(task_id, sum)

        cv_model = await crud.get_cv_model(CVModelEnum.YOLO8M)

        await crud.subtract_from_user_token_amount(user_name, cv_model.cost)

        user_id = await crud.get_user_id(user_name)

        await crud.add_image_history(ImageHistorySchema(

            user_id=user_id,
            task_id=task_id
        ))


    @dramatiq.actor
    @dramatiq.asyncio.async_to_sync
    @staticmethod
    async def use_yolo8n(user_name: str, task_id: int, image_path: str):

        utils_method = UtilsMethod()
        
        # TODO: Реализация работы с моделью

        image_bytes = utils_method.read_image(image_path)

        sum, _, _ = CVModel.Yolo8N_Work(task_id, image_bytes)

        async_generator = SQLAlchemyDBHelper().get_async_session()

        session = await async_generator.__anext__()

        crud = SQLAlchemyCRUD(session)

        task: TaskId = await crud.get_task_by_id(task_id)

        await crud.update_task_result(task.msg_id, str(Path(f'database\\images\\processed\\{task_id}Result.jpeg')))

        await crud.update_task_result_sum(task_id, sum)

        cv_model = await crud.get_cv_model(CVModelEnum.YOLO8M)

        await crud.subtract_from_user_token_amount(user_name, cv_model.cost)

        user_id = await crud.get_user_id(user_name)

        await crud.add_image_history(ImageHistorySchema(

            user_id=user_id,
            task_id=task_id
        ))