from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import database

from dictionary.schemas import WordCreate, WordUpdate
from dictionary.services import (
    create_word,
    get_word as get_word_orm,
    delete_word as delete_word_orm,
    update_word as update_word_orm,
)

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


@router.get('/word/{word_id}')
async def get_word(
    word_id: int,
    user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(database.session_dependency),
):
    word = await get_word_orm(word_id=word_id, user_id=user.id, session=session)

    if word is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Object not found')

    return word


@router.delete('/word/{word_id}')
async def delete_word(
    word_id: int,
    user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(database.session_dependency),
):
    # try:
    #     await delete_word_orm(
    #         word_id=word_id,
    #         user_id=user.id,
    #         session=session
    #     )
    # except:
    # raise HTTPException(
    #     status_code=status.HTTP_404_NOT_FOUND,
    #     detail='Object is not found.'
    # )

    # return {'message': 'Object is successfully deleted.'}
    deleted = await delete_word_orm(word_id=word_id, user_id=user.id, session=session)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Object not found.'
        )

    return {'message': 'Object successfully deleted.'}


@router.patch('/word/{word_id}')
async def update_word(
    word_id: int,
    update_data: WordUpdate,
    user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(database.session_dependency),
):
    word = await update_word_orm(
        word_id=word_id,
        user_id=user.id,
        update_data=update_data,
        session=session,
    )

    if word is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Object not found.'
        )

    return word
