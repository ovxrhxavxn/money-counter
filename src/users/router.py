from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

from .schemas import User, UserDate
from .services import UserService
from .dependencies import get_user_service


router = APIRouter(

    prefix='/users',
    tags=['User']
)


@router.post('/')
async def add_user(
    
    user: User,
    service: Annotated[UserService, Depends(get_user_service)]
    
    ):

    try:

        await service.add(user)

    except IntegrityError:

        raise HTTPException(400, detail='The user`s name already exists')
    

@router.get('/{user_name}', response_model=User)
async def get_user(
    
    user_name: str,
    service: Annotated[UserService, Depends(get_user_service)]

    ):

    try:

        return await service.get_by_name(user_name)

    except IndexError:

        raise HTTPException(404, detail='The user doesn`t exist')
    

@router.get('/', response_model=list[UserDate])
async def get_all_users(service: Annotated[UserService, Depends(get_user_service)]):

    return await service.get_all()
    

@router.patch('/{user_name}/tokens')
async def change_user_token_amount(
    
    user_name: str, 
    token_amount: int,
    service: Annotated[UserService, Depends(get_user_service)]
    
    ):

    await service.change_token_amount(user_name, token_amount)


@router.patch('/{user_name}/role')
async def change_user_role(
    
    user_name: str, 
    new_role: str,
    service: Annotated[UserService, Depends(get_user_service)]
    
    ):

    await service.change_role(user_name, new_role)