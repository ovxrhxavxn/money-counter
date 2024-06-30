from fastapi import APIRouter
from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from .schemas import User as UserSchema
from database.database import get_async_session
from database import crud


router = APIRouter(

    prefix='/users',
    tags=['User']
)

@router.post('/')
async def add_new_user(user: UserSchema, session: AsyncSession = Depends(get_async_session)):

    try:

        await crud.add_new_user(session, user)

    except IntegrityError:

        raise HTTPException(404, detail='The user doesn`t exist')


@router.get('/{user_name}', response_model=UserSchema)
async def get_user_data(user_name: str, session: AsyncSession = Depends(get_async_session)):

    try:

        return await crud.get_user(session, user_name)
    
    except IntegrityError:

        raise HTTPException(400, detail='The user`s name already exists')