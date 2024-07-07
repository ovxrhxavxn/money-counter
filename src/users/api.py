from fastapi import APIRouter
from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from .schemas import UserSchema, UserDate
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

            await SQLAlchemyCRUD(session).add_user(user)

        except IntegrityError:

            raise HTTPException(400, detail='The user`s name already exists')
        

    @staticmethod
    @__ROUTER.get('/{user_name}', response_model=UserSchema)
    async def get_user(user_name: str, session: AsyncSession = Depends(SQLAlchemyDBHelper().get_async_session)):

        try:

            return await SQLAlchemyCRUD(session).get_user(user_name)
    
        except IndexError:

            raise HTTPException(404, detail='The user doesn`t exist')
        

    @staticmethod
    @__ROUTER.get('/', response_model=list[UserDate])
    async def get_all_users(session: AsyncSession = Depends(SQLAlchemyDBHelper().get_async_session)):

        return await SQLAlchemyCRUD(session).get_all_users()
        

    @staticmethod
    @__ROUTER.patch('/{user_name}/tokens')
    async def change_user_token_amount(user_name: str, token_amount: int, session: AsyncSession = Depends(SQLAlchemyDBHelper().get_async_session)):

        await SQLAlchemyCRUD(session).change_user_token_amount(user_name, token_amount)

    
    @staticmethod
    @__ROUTER.patch('/{user_name}/role')
    async def change_user_role(user_name: str, new_role: str, session: AsyncSession = Depends(SQLAlchemyDBHelper().get_async_session)):

        await SQLAlchemyCRUD(session).change_user_role(user_name, new_role)