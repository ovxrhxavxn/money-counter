from sqlalchemy.orm import Mapped, mapped_column

from database.orm.sqlalchemy.stuff import Base
from database.annotated_types import (

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