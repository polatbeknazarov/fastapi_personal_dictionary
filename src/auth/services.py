from fastapi import HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.schemas import UserCreate
from auth.utils import get_hashed_password


async def get_user(session: AsyncSession, username: str, email: str = None) -> User | None:
    try:
        query = select(User).filter(or_(
            User.username == username,
            User.email == email,
        ))
        result = await session.execute(query)

        return result.scalar_one_or_none()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def create_user(session: AsyncSession, user: UserCreate) -> User:
    try:
        hashed_password = get_hashed_password(user.password)

        user_obj = User(
            username=user.username.lower(),
            email=user.email.lower(),
            first_name=user.first_name.title(),
            last_name=user.last_name.title(),
            hashed_password=hashed_password,
        )

        session.add(user_obj)
        await session.commit()
        await session.refresh(user_obj)

        return user_obj
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
