from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.schemas import UserCreate
from auth.utils import get_hashed_password


async def get_user(session: AsyncSession, email: str) -> User | None:
    query = select(User).filter(User.email == email)
    result = await session.execute(query)

    return result.scalar_one_or_none()


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
