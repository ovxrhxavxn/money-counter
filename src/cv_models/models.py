from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from database.database import Base
from database.annotated_type import (

    intpk,
    utcnow
)
from .schemas import CVModelEnum


class CVModelTable(Base):

    __tablename__ = 'cv_models'

    id: Mapped[intpk]
    name: Mapped[CVModelEnum] = mapped_column(unique=True)
    cost: Mapped[int]


class ImageHistory(Base):

    __tablename__ = 'image_histories'

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'))
    date: Mapped[utcnow]


class Task(Base):

    __tablename__ = 'tasks'
    
    id: Mapped[intpk]
    cv_model_id: Mapped[int] = mapped_column(ForeignKey('cv_models.id'))
    msg_id: Mapped[int] = mapped_column(unique=True)
    result_path: Mapped[str]
    result_sum: Mapped[float | None]