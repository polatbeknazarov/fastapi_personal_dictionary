from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from dictionary.models import Word
from dictionary.schemas import WordCreate


async def create_word(
    word: WordCreate,
    user_id: int,
    session: AsyncSession,
) -> Word | None:
    try:
        word_obj = Word(
            user_id=user_id,
            word=word.word,
            translation=word.translation,
            image_url=word.image_url,
            examples=word.examples,
        )

        session.add(word_obj)
        await session.commit()
        await session.refresh(word_obj)

        return word_obj
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def get_word(word_id: int, user_id: int, session: AsyncSession) -> Word | None:
    word = select(Word).filter(Word.user_id == user_id, Word.id == word_id)
    result = await session.execute(word)

    return result.scalar_one_or_none()


async def delete_word(word_id: int, user_id: int, session: AsyncSession) -> bool:
    # word = delete(Word).filter(
    #     Word.user_id == user_id, Word.id == word_id
    # )

    # await session.execute(word)
    # await session.commit()
    word = await get_word(word_id=word_id, user_id=user_id, session=session)

    if word is not None:
        await session.delete(word)
        await session.commit()

        return True

    return False


async def update_word(word_id: int, user_id: int, update_data: dict, session: AsyncSession) -> Word | None:
    word = await get_word(word_id=word_id, user_id=user_id, session=session)
    update_data = update_data.dict(exclude_unset=True)

    if word:
        for field, value in update_data.items():
            setattr(word, field, value)
        await session.commit()
        await session.refresh(word)

        return word

    return None
