from pydantic import BaseModel, Field

from roles.schemas import Role


class UserSchema(BaseModel):

    name: str
    role: Role
    token_amount: int