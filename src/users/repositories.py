from sqlalchemy import select, update

from database.orm.sqlalchemy.repository import SQLAlchemyRepository
from database.orm.sqlalchemy.stuff import async_session_maker
from .models import User
from .schemas import UserSchema, UserDate


class UserRepository(SQLAlchemyRepository):

    model = User
    
    async def get(self, name: str):

        async with async_session_maker() as session:

            query = select(self.model).where(self.model.name == name)

            result = await session.execute(query)

            user_from_db = result.all()[0].t[0]

            user = UserSchema(

                name=user_from_db.name,
                role=user_from_db.role,
                token_amount=user_from_db.token_amount
            )

            return user
    

    async def get_all(self) -> list[UserDate]:

        users = []

        async with async_session_maker() as session:

            users_query = select(self.model)

            users_result = await session.execute(users_query)

            users_from_db = users_result.all()

            for i, row in enumerate(users_from_db):

                for j, user in enumerate(row.t):

                    users.append(

                        UserDate(

                            name=user.name,
                            role=user.role,
                            token_amount=user.token_amount,
                            registration_date=user.registration_date
                        )
                    )

        return users
    

    async def subtract_from_user_token_amount(self, name: str, cost: int):

        user = await self.get_by_name(name)

        async with async_session_maker() as session:

            stmt = update(self.model).where(self.model.name == name).values(token_amount = user.token_amount - cost) 

            await session.execute(stmt)
            await session.commit()

    
    async def change_token_amount(self, name: str, new_value: int):

        async with async_session_maker() as session:

            stmt = update(self.model).where(self.model.name == name).values(token_amount = new_value) 

            await session.execute(stmt)
            await session.commit()


    async def change_role(self, name: str, new_role: str):

        async with async_session_maker() as session:
                
            stmt = update(self.model).where(self.model.name == name).values(role = new_role) 

            await session.execute(stmt)
            await session.commit()


    async def get_id(self, user_name: str):

        async with async_session_maker() as session:

            query = select(self.model).where(self.model.name == user_name)

            result = await session.execute(query)

        user_from_db = result.all()[0].t[0]

        return user_from_db.id