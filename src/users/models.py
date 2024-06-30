from sqlalchemy import Integer, String, Column

from database.database import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False)
    token_amount = Column(Integer, nullable=False)