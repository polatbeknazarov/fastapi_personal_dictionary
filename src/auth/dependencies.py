from fastapi import Form, HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import InvalidTokenError

from database import database
from auth.services import get_user
from auth.utils import verify_password, decode_jwt
from auth.schemas import UserSchema


http_bearer = HTTPBearer()


async def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
        session: AsyncSession = Depends(database.session_dependency),
):
    user = await get_user(session=session, username=username)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User is not active',
        )

    return user


async def get_current_auth_user(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        session: AsyncSession = Depends(database.session_dependency)
) -> UserSchema:
    token = credentials.credentials
    try:
        payload = decode_jwt(token=token)
        username: str | None = payload.get('sub')
        user = await get_user(session=session, username=username)
        if user:
            return user
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')


async def get_current_user(user: UserSchema = Depends(get_current_auth_user)):
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User is not active'
        )

    return user