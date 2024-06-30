from pydantic import BaseModel, Field
from enum import StrEnum


class RoleEnum(StrEnum):

    CLIENT = 'client'
    MANAGER = 'manager'