from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from users.models import User as UserModel
from users.schemas import UserSchema
from cv_models.models import Task, ImageHistory, CVModel
from cv_models.schemas import TaskSchema, TaskId, ImageHistorySchema, CVModelSchema, CVModelEnum

class SQLAlchemyCRUD:

    def __init__(self, db_session: AsyncSession):

        self._db_session = db_session

    async def add_user(self, user: UserSchema):

        stmt = insert(UserModel).values(**user.model_dump())

        await self._db_session.execute(stmt)
        await self._db_session.commit()

    
    async def get_user(self, user_name: str) -> UserSchema:

        query = select(UserModel).where(UserModel.name == user_name)

        result = await self._db_session.execute(query)

        user_from_db = result.all()[0].t[0]

        user = UserSchema(

            name=user_from_db.name,
            role=user_from_db.role,
            token_amount=user_from_db.token_amount
        )

        return user
    
    
    async def update_user_token_amount(self, user_name: str, cost: int):

        user = await self.get_user(user_name)

        stmt = update(UserModel).where(UserModel.name == user_name).values(token_amount = user.token_amount - cost) 

        await self._db_session.execute(stmt)
        await self._db_session.commit()

    
    async def add_task(self, task: TaskSchema):
        
        stmt = insert(Task).values(**task.model_dump())

        await self._db_session.execute(stmt)
        await self._db_session.commit()

    
    async def get_task_by_id(self, task_id: int):
        
        query = select(Task).where(Task.id == task_id)

        result = await self._db_session.execute(query)

        task_from_db = result.all()[0].t[0]

        task = TaskId(

            id=task_from_db.id,
            cv_model_id=task_from_db.cv_model_id,
            msg_id=task_from_db.msg_id,
            result_path=task_from_db.result_path
        )

        return task
    
    async def get_task_by_msg_id(self, msg_id: str):
        
        query = select(Task).where(Task.msg_id == msg_id)

        result = await self._db_session.execute(query)

        task_from_db = result.all()[0].t[0]

        task = TaskId(

            id=task_from_db.id,
            cv_model_id=task_from_db.cv_model_id,
            msg_id=task_from_db.msg_id,
            result_path=task_from_db.result_path
        )

        return task
    
    async def update_task_result(self, msg_id: str, new_result: str):

        stmt = update(Task).where(Task.msg_id == msg_id).values(result_path=new_result)

        await self._db_session.execute(stmt)
        await self._db_session.commit()

    
    async def get_last_task(self):

        query = select(Task).order_by(Task.id.desc())

        result = await self._db_session.execute(query)

        task_from_db = result.all()[0].t[0]

        task = TaskId(

            id=task_from_db.id,
            cv_model_id=task_from_db.cv_model_id,
            msg_id=task_from_db.msg_id,
            result_path=task_from_db.result_path
        )

        return task
    
    async def update_task_msg_id(self, task_id: int, new_msg_id: str):

        stmt = update(Task).where(Task.id == task_id).values(msg_id = new_msg_id)

        await self._db_session.execute(stmt)
        await self._db_session.commit()

    
    async def delete_task(self, task_id: int):

        stmt = delete(Task).where(Task.id == task_id)

        await self._db_session.execute(stmt)
        await self._db_session.commit()


    async def add_image_history(self, img_his: ImageHistorySchema):

        stmt = insert(ImageHistory).values(**img_his.model_dump())

        await self._db_session.execute(stmt)
        await self._db_session.commit()

    async def get_user_id(self, user_name: str):

        query = select(UserModel).where(UserModel.name == user_name)

        result = await self._db_session.execute(query)

        user_from_db = result.all()[0].t[0]

        return user_from_db.id
    
    async def add_cv_model(self, cv_model: CVModelSchema):

        stmt = insert(CVModel).values(**cv_model.model_dump())

        await self._db_session.execute(stmt)
        await self._db_session.commit()

    
    async def get_cv_model(self, model_name: str):

        query = select(CVModel).where(CVModel.name == model_name)

        result = await self._db_session.execute(query)

        model_from_db = result.all()[0].t[0]

        model = CVModelSchema(

            name=model_from_db.name,
            cost=model_from_db.cost
        )

        return model
    
    
    async def get_cv_model_id(self, model_name: str):

        query = select(CVModel).where(CVModel.name == model_name)

        result = await self._db_session.execute(query)

        model_from_db = result.all()[0].t[0]

        return model_from_db.id
    

    async def fill_cv_model_table(self):

        for i, model in enumerate(CVModelEnum):

                await self.add_cv_model(CVModelSchema(

                    name=model,
                    cost=(1+i)*5
                ))