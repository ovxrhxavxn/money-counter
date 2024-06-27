from fastapi import APIRouter

from .schemas import User


router = APIRouter(

    prefix='/users',
    tags=['User']
)

@router.post('/')
async def register_user(user: User):

    pass

@router.get('/{user_name}', response_model=User)
async def get_user(user_name: str):

    pass