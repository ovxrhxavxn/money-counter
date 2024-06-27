from pydantic import BaseModel, Field
from enum import StrEnum

class Role(StrEnum):

    MANAGER = 'manager'
    CLIENT = 'client'

class User(BaseModel):

    name: str
    role: Role
    token_amount: int