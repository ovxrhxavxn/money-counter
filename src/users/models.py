from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, ForeignKey, Column


Base = declarative_base()


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    token_amount = Column(Integer, nullable=False)


class Role(Base):

    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(15), nullable=False)


class UserRole(Base):

    __tablename__ = 'users_roles'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)