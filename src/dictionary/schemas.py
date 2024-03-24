from pydantic import BaseModel


class WordCreate(BaseModel):
    word: str
    translation: str
    image_url: str
    examples: str
