from datetime import datetime
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
)
from sqlalchemy.orm import relationship

from database import Base


class Word(Base):
    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey('users.id'))
    word: str = Column(String, nullable=False)
    translation: str = Column(String, nullable=False)
    image_url: str = Column(String,  nullable=True)
    examples: str = Column(Text, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow,
                                  onupdate=datetime.utcnow)

    owner = relationship('User', back_populates='words')
