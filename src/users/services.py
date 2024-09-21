from roles.schemas import Role
from .repositories import UserRepository
from .schemas import UserSchema


class UserService:

    def __init__(self, user_repo: type[UserRepository]) -> None:

        self._user_repo = user_repo()

    
    async def add(self, schema: UserSchema):
    
        user_dict = schema.model_dump()

        await self._user_repo.add(user_dict)

        
    async def delete(self, id: int):

        await self._user_repo.delete(id)
    
    
    async def get_by_name(self, name: str) -> UserSchema:

        return await self._user_repo.get(name)
    

    async def get_all(self):

        return await self._user_repo.get_all()


    async def change_token_amount(self, user_name: str, new_value: int):

        await self._user_repo.change_token_amount(user_name, new_value)


    async def change_role(self, user_name: str, new_role: Role):

        await self._user_repo.change_role(user_name, new_role)