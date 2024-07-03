from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from users.models import User as UserModel
from users.schemas import UserSchema
from cv_models.models import Task
from cv_models.schemas import TaskSchema, TaskId

class SQLAlchemyCRUD:

    async def add_user(self, db_session: AsyncSession, user: UserSchema):

        stmt = insert(UserModel).values(**user.model_dump())

        await db_session.execute(stmt)
        await db_session.commit()

    
    async def get_user(self, db_session: AsyncSession, user_name: str) -> UserSchema:

        query = select(UserModel).where(UserModel.name == user_name)

        result = await db_session.execute(query)

        user_from_db = result.all()[0].t[0]

        user = UserSchema(

            name=user_from_db.name,
            role=user_from_db.role,
            token_amount=user_from_db.token_amount
        )

        return user
    
    
    async def update_user_token_amount(self, db_session: AsyncSession, user_name: str, cost: int):

        user = await self.get_user(db_session, user_name)

        stmt = update(UserModel).where(UserModel.name == user_name).values(token_amount = user.token_amount - cost) 

        await db_session.execute(stmt)
        await db_session.commit()

    
    async def add_task(self, db_session: AsyncSession, task: TaskSchema):
        
        stmt = insert(Task).values(**task.model_dump())

        await db_session.execute(stmt)
        await db_session.commit()

    
    async def get_task_by_id(self, db_session: AsyncSession, task_id: int):
        
        query = select(Task).where(Task.id == task_id)

        result = await db_session.execute(query)

        task_from_db = result.all()[0].t[0]

        task = TaskId(

            id=task_from_db.id,
            msg_id=task_from_db.msg_id,
            result_path=task_from_db.result_path
        )

        return task
    
    async def get_task_by_msg_id(self, db_session: AsyncSession, msg_id: str):
        
        query = select(Task).where(Task.msg_id == msg_id)

        result = await db_session.execute(query)

        task_from_db = result.all()[0].t[0]

        task = TaskId(

            id=task_from_db.id,
            msg_id=task_from_db.msg_id,
            result_path=task_from_db.result_path
        )

        return task
    
    async def update_task_result(self, db_session: AsyncSession, msg_id: str, new_result: str):

        stmt = update(Task).where(Task.msg_id == msg_id).values(result_path=new_result)

        await db_session.execute(stmt)
        await db_session.commit()

    
    async def get_last_task(self, db_session: AsyncSession):

        query = select(Task).order_by(Task.id.desc())

        result = await db_session.execute(query)

        task_from_db = result.all()[0].t[0]

        task = TaskId(

            id=task_from_db.id,
            msg_id=task_from_db.msg_id,
            result_path=task_from_db.result_path
        )

        return task
    
    async def update_task_msg_id(self, db_session: AsyncSession, task_id: int, new_msg_id: str):

        stmt = update(Task).where(Task.id == task_id).values(msg_id = new_msg_id)

        await db_session.execute(stmt)
        await db_session.commit()

    
    async def delete_task(self, db_session: AsyncSession, task_id: int):

        stmt = delete(Task).where(Task.id == task_id)

        await db_session.execute(stmt)
        await db_session.commit()