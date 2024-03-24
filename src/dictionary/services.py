from sqlalchemy.ext.asyncio import AsyncSession

from dictionary.models import Word
from dictionary.schemas import WordCreate


async def create_word(
    word: WordCreate,
    user_id: int,
    session: AsyncSession,
):
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
