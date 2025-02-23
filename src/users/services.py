from roles.enums import Role
from database.repositories import AbstractUserRepository
from .schemas import UserDate, User


class UserService:

    def __init__(self, user_repo: type[AbstractUserRepository]) -> None:
        self._user_repo = user_repo()

    
    async def add(self, schema: User):
        user_dict = schema.model_dump()

        await self._user_repo.add(user_dict)

        
    async def delete(self, id: int):
        await self._user_repo.delete(id)
    
    
    async def get_by_name(self, name: str) -> UserDate:
        user = await self._user_repo.get(name)

        return UserDate.model_validate(user)
    

    async def get_all(self):
        rows = await self._user_repo.get_all()

        return [UserDate.model_validate(row[0]) for row in rows]


    async def change_token_amount(self, user_name: str, new_value: int):
        await self._user_repo.change_token_amount(user_name, new_value)


    async def change_role(self, user_name: str, new_role: Role):
        await self._user_repo.change_role(user_name, new_role)


    async def get_id(self, name: str) -> int:
        await self._user_repo.get_id(name)