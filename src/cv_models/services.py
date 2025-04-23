from pathlib import Path
import base64

from fastapi.exceptions import HTTPException
from sqlalchemy.exc import NoResultFound

from database.repositories import (

    AbstractCVModelRepository,
    AbstractTaskRepository
)
from .schemas import TaskId, CVModelSchema


class CVModelsService:

    def __init__(
            
            self, 
            cv_model_repo: type[AbstractCVModelRepository]
            
            ):

        self._cv_model_repo = cv_model_repo()
    

    async def get(self, name: str):

        try:
            return await self._cv_model_repo.get(name)
        
        except NoResultFound:
            raise HTTPException(404, detail='The model doesn`t exist!')
    

    async def get_all(self):
        rows = await self._cv_model_repo.get_all()

        return [CVModelSchema.model_validate(row[0]) for row in rows]
    
    
    async def change_cost(self, name: str, new_value: int):
        await self._cv_model_repo.change_cost(name, new_value)

    
    async def fill_table_once(self):

        models = await self.get_all()
        
        if len(models) == 0:
            return

        await self._cv_model_repo.fill_table()


    async def get_id(self, name: str):
        return await self._cv_model_repo.get_id(name)


class TasksService:

    def __init__(self, task_repo: type[AbstractTaskRepository]):
        self._task_repo = task_repo()


    async def add(self, schema: dict):
        await self._task_repo.add(schema)


    async def get(self, id: int):
        task = await self._task_repo.get(id)

        return TaskId.model_validate(task)


    async def get_by_msg_id(self, msg_id: str):
        task = await self._task_repo.get_by_msg_id(msg_id)

        return TaskId.model_validate(task)
    
    
    async def delete(self, id: int):
        await self._task_repo.delete(id)


    async def update_result(self, msg_id: str, new_result: str):
        await self._task_repo.update_result(msg_id, new_result)


    async def get_last(self):
        last_task = await self._task_repo.get_last()

        return TaskId.model_validate(last_task)
    

    async def update_msg_id(self, id: int, new_msg_id: str):
        await self._task_repo.update_msg_id(id, new_msg_id)

    
    async def update_result_sum(self, id: int, new_sum: int):
        await self._task_repo.update_result_sum(id, new_sum)


    async def check_task_result(self, msg_id: str):
        task = await self._task_repo.get_by_msg_id(msg_id)

        if not task.image_id:
            raise HTTPException(202, detail="The task is in processing")
        
        img_bytes = await (Path(task.image_id).resolve())

        encoded_string = base64.b64encode(img_bytes).decode()

        return {

            'image' : encoded_string,
            'total' : task.result_sum
        }