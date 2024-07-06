from sqlalchemy import Integer, String, Column, Date
from datetime import datetime as dt, UTC

from database.database import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False)
    token_amount = Column(Integer, nullable=False, )
    registration_date = Column(Date, nullable=False, default=dt.now(UTC).date())