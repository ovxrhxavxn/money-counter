from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.orm.sqlalchemy.stuff import Base
from database.orm.sqlalchemy.annotated_types import (

    intpk,
    utcnow
)
from roles.enums import Role


class User(Base):

    __tablename__ = 'users'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
    role: Mapped[Role]
    token_amount: Mapped[int]
    registration_date: Mapped[utcnow]


class CVModelTable(Base):

    __tablename__ = 'cv_models'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
    cost: Mapped[int]


class TaskHistory(Base):

    __tablename__ = 'task_histories'

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'))
    date: Mapped[utcnow]


class Task(Base):

    __tablename__ = 'tasks'
    
    id: Mapped[intpk]
    cv_model_id: Mapped[int] = mapped_column(ForeignKey('cv_models.id'), nullable=True)
    msg_id: Mapped[int] = mapped_column(unique=True, nullable=True)
    image_id: Mapped[int] = mapped_column(ForeignKey('images.id'), nullable=True)
    result_sum: Mapped[float] = mapped_column(nullable=True)


class Image(Base):

    __tablename__ = 'images'

    id: Mapped[intpk]
    path: Mapped[str] = mapped_column(nullable=True)