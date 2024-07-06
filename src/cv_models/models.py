from sqlalchemy import Integer, String, Column, ForeignKey, Date
from datetime import datetime as dt
from datetime import UTC

from database.database import Base


class CVModel(Base):

    __tablename__ = 'cv_models'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    cost = Column(Integer, nullable=False)


class ImageHistory(Base):

    __tablename__ = 'image_histories'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    task_id = Column(String, ForeignKey('tasks.id'))
    date = Column(Date, nullable=False, default=dt.now(UTC).date())


class Task(Base):

    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    cv_model_id = Column(Integer, ForeignKey('cv_models.id'))
    msg_id = Column(String, nullable=True, unique=True)
    result_path = Column(String, nullable=True)