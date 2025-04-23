from sqlalchemy.exc import NoResultFound
from fastapi.exceptions import HTTPException

from roles.enums import Role
from database.repositories import AbstractUserRepository
from .schemas import UserDate, User


class UsersService:

    def __init__(self, user_repo: type[AbstractUserRepository]) -> None:
        self._user_repo = user_repo()

    async def get(self, name: str):
        user = await self._user_repo.get(name)

        return UserDate.model_validate(user)


    async def add(self, schema: User):
        user_dict = schema.model_dump()

        await self._user_repo.add(user_dict)

        
    async def delete(self, id: int):
        await self._user_repo.delete(id)
    
    
    async def get_by_name(self, name: str) -> UserDate:

        try: 
            user = await self._user_repo.get(name)

        except NoResultFound:
            raise HTTPException(404, detail='The user doesn`t exist')

        return UserDate.model_validate(user)
    

    async def get_all(self):
        rows = await self._user_repo.get_all()

        return [UserDate.model_validate(row[0]) for row in rows]


    async def change_token_amount(self, user_name: str, new_value: int):
        await self._user_repo.change_token_amount(user_name, new_value)


    async def subtract_from_token_amount(self, name: str, cost: int):
        await self._user_repo.subtract_from_token_amount(name, cost)


    async def change_role(self, user_name: str, new_role: Role):
        await self._user_repo.change_role(user_name, new_role)


    async def get_id(self, name: str) -> int:
        await self._user_repo.get_id(name)