from fastapi import APIRouter
from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from .schemas import UserSchema as UserSchema
from database.database import SQLAlchemyDBHelper
from database.crud import SQLAlchemyCRUD

class UserAPI:

    __ROUTER = APIRouter(

        prefix='/users',
        tags=['User']
    )

    @property
    def router(self):
        return self.__ROUTER

    @staticmethod
    @__ROUTER.post('/')
    async def add_user(user: UserSchema, session: AsyncSession = Depends(SQLAlchemyDBHelper().get_async_session)):

        try:

            await SQLAlchemyCRUD().add_user(session, user)

        except IntegrityError:

            raise HTTPException(400, detail='The user`s name already exists')
        

    @staticmethod
    @__ROUTER.get('/{user_name}', response_model=UserSchema)
    async def get_user(user_name: str, session: AsyncSession = Depends(SQLAlchemyDBHelper().get_async_session)):

        try:

            return await SQLAlchemyCRUD().get_user(session, user_name)
    
        except IndexError:

            raise HTTPException(404, detail='The user doesn`t exist')
        