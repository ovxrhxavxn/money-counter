from sqlalchemy import Integer, String, Column, ForeignKey, Date
from datetime import datetime as dt

from database.database import Base


class ImageHistory(Base):

    __tablename__ = 'image_histories'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    image_path = Column(String, nullable=False)
    date = Column(Date, nullable=False, default=dt.now(dt.UTC).date())