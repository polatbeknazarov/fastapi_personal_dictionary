from typing import Optional
from pydantic import BaseModel, Field


class WordCreate(BaseModel):
    word: str
    translation: str
    image_url: str
    examples: str


class WordUpdate(BaseModel):
    word: Optional[str] = Field(None, min_length=1, max_length=255)
    translation: Optional[str] = Field(None, min_length=1, max_length=255)
    image_url: Optional[str] = Field(None, min_length=1, max_length=255)
    examples: Optional[str] = None
