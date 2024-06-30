from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException

from users.models import User as UserModel
from users.schemas import User as UserSchema


async def add_new_user(db_session: AsyncSession, user: UserSchema):

    stmt = insert(UserModel).values(**user.model_dump())

    await db_session.execute(stmt)
    await db_session.commit()

    
async def get_user(db_session: AsyncSession, user_name: str):

    query = select(UserModel).where(UserModel.name == user_name)

    result = await db_session.execute(query)

    user_from_db = result.all()[0].t[0]

    user = UserSchema(

        name=user_from_db.name,
        role=user_from_db.role,
        token_amount=user_from_db.token_amount
    )

    return user