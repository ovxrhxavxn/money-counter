from pydantic import BaseModel, Field

from roles.schemas import RoleEnum


class User(BaseModel):

    name: str
    role: RoleEnum
    token_amount: int