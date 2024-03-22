from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from database import database
from auth.schemas import (
    UserCreate,
    UserSchema,
    Token,
    UserRead,
)
from auth.services import get_user, create_user
from auth.utils import encode_jwt
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
    access = encode_jwt(jwt_payload)

    return Token(
        access_token=access,
        token_type='Bearer',
    )


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
