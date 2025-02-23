from datetime import date

from pydantic import BaseModel

from roles.enums import Role


class User(BaseModel):

    name: str
    role: Role
    token_amount: int


class UserFromDB(User):

    id: int


class UserDate(User):

    registration_date: date

    class Config:
        from_attributes = True