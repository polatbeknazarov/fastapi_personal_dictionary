from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import database
from auth.schemas import UserCreate
from auth.services import get_user, create_user


router = APIRouter(tags=['auth'])


@router.post('/register', response_model=None)
async def register_user(user: UserCreate, session: AsyncSession = Depends(database.session_dependency)):
    existing_user = await get_user(session=session, email=user.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists.')

    await create_user(session=session, user=user)

    return {'message': 'User successfully created.'}
