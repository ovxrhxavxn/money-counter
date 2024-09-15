from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text

from database.database import Base
from database.annotated_type import (

    intpk,
    utcnow
)
from roles.schemas import Role


class User(Base):

    __tablename__ = 'users'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
    role: Mapped[Role]
    token_amount: Mapped[int]
    registration_date: Mapped[utcnow]