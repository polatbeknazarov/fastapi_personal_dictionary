from fastapi import Form, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.schemas import UserCreate


async def get_user(session: AsyncSession, username: str) -> User | None:
    query = select(User).filter(User.username == username)
    result = await session.execute(query)

    return result.scalar_one_or_none()


from auth.utils import get_hashed_password

async def create_user(session: AsyncSession, user: UserCreate) -> User:
    hashed_password = get_hashed_password(user.password)

    user = User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
