import jwt

from datetime import datetime, timedelta
from fastapi import Form, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from config import password_context, settings
from database import database
from auth.services import get_user
from auth.schemas import UserSchema


http_bearer = HTTPBearer()


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def encode_jwt(
        payload: dict,
        private_key: str = settings.PRIVATE_KEY_PATH.read_text(),
        algorithm: str = settings.ALGORITHM,
        expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
):
    to_encode = payload.copy()

    now = datetime.utcnow()
    expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=expire,
        iat=now,
    )

    encoded = jwt.encode(
        payload=to_encode, key=private_key, algorithm=algorithm)

    return encoded


def decode_jwt(token: str | bytes, publick_key: str = settings.PUBLICK_KEY_PATH.read_text(), algorithm: str = settings.ALGORITHM):
    decoded = jwt.decode(jwt=token, key=publick_key, algorithms=[algorithm])

    return decoded


async def validate_auth_user(username: str = Form(), password: str = Form(), session: AsyncSession = Depends(database.session_dependency)):
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid username or password'
    )

    user = await get_user(session=session, username=username)

    if not user:
        raise unauthorized_exception

    if not verify_password(password=password, hashed_password=user.hashed_password):
        raise unauthorized_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User is not active',
        )

    return user


async def get_current_auth_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer), session: AsyncSession = Depends(database.session_dependency)) -> UserSchema:
    token = credentials.credentials
    payload = decode_jwt(token=token)

    username: str | None = payload.get('sub')

    get_user_from_db = await get_user(session=session, username=username)

    if get_user_from_db:
        return get_user_from_db

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')


async def get_current_user(user: UserSchema = Depends(get_current_auth_user)):
    if user.is_active:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='User is not active'
    )
