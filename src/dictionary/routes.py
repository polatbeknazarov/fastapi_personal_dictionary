from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import database
from dictionary.schemas import WordCreate
from dictionary.services import create_word
from auth.dependencies import get_current_user
from auth.schemas import UserSchema


router = APIRouter(tags=['dictionary'])


@router.post('/word')
async def add_word(
    word: WordCreate,
    user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(database.session_dependency),
):
    new_word = await create_word(word=word, user_id=user.id, session=session)

    return new_word
