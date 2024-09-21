from datetime import date

from pydantic import BaseModel

from roles.schemas import Role


class UserSchema(BaseModel):

    name: str
    role: Role
    token_amount: int


class UserId(UserSchema):

    id: int


class UserDate(UserSchema):

    registration_date: date