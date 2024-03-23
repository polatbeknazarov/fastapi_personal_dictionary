from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from database import database
from auth.schemas import (
    UserCreate,
    UserSchema,
    Token,
    UserRead,
)
from auth.services import create_user, get_user
from auth.utils import encode_access_jwt, encode_refresh_jwt, decode_jwt
from auth.dependencies import (
    validate_auth_user,
    get_current_user,
    validate_registration,
)


router = APIRouter(prefix='/users', tags=['auth',])


@router.post('/register')
async def register_user(
    user: UserCreate = Depends(validate_registration),
    session: AsyncSession = Depends(database.session_dependency),
):
    '''
    Register a new user.
    '''
    await create_user(session=session, user=user)

    return {'message': 'User successfully created.'}


@router.post('/login', response_model=Token)
async def login_user(user: UserSchema = Depends(validate_auth_user)):
    '''
    Generate JWT token.
    '''
    jwt_payload = {
        'sub': user.username,
    }
    access = encode_access_jwt(jwt_payload)
    refresh = encode_refresh_jwt(jwt_payload)

    return Token(
        access_token=access,
        refresh_token=refresh,
        token_type='Bearer',
    )


@router.post('/token/refresh')
async def refresh_access_token(refresh_token: str, session: AsyncSession = Depends(database.session_dependency),):
    try:
        payload = decode_jwt(token=refresh_token)
        username: str = payload.get('sub')
        print('##!@#!@#!@#!@#!@#!@#!@#@!#', username, payload.get('token_type'))

        if username is None or payload.get('token_type') != 'refresh_token':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')

    user = await get_user(session=session, username=username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    jwt_payload = {
        'sub': user.username,
    }

    access_token = encode_access_jwt(payload=jwt_payload)

    return {
        'access_token': access_token,
    }


@router.get('/me', response_model=UserRead)
async def user_check_info(
    user: UserSchema = Depends(get_current_user),
):
    '''
    Get current user's information.
    '''
    return UserRead(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
    )
