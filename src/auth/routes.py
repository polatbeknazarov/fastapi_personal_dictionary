from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import database
from auth.schemas import UserCreate, UserSchema, Token
from auth.services import get_user, create_user
from auth.utils import encode_jwt
from auth.dependencies import validate_auth_user, get_current_user, get_user_token_payload


router = APIRouter(tags=['auth'])


@router.post('/register', response_model=None)
async def register_user(
    user: UserCreate,
    session: AsyncSession = Depends(database.session_dependency),
):
    existing_user = await get_user(session=session, username=user.username)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists.')

    await create_user(session=session, user=user)

    return {'message': 'User successfully created.'}


@router.post('/login', response_model=Token)
async def login_user(user: UserSchema = Depends(validate_auth_user)):
    jwt_payload = {
        'sub': user.username,
    }
    access = encode_jwt(jwt_payload)

    return Token(
        access_token=access,
        token_type='Bearer',
    )


@router.get('/users/me')
async def user_check_info(
    user: UserSchema = Depends(get_current_user),
    payload: dict = Depends(get_user_token_payload),
):
    iat = payload.get('iat')
    logged_in = datetime.fromtimestamp(iat)

    return {
        'username': user.username,
        'logged_in': logged_in,
    }
