from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean

from database import Base


class User(Base):
    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(50), unique=True, nullable=False)
    email: str = Column(String(100), nullable=False, unique=True)
    first_name: str = Column(String(100), nullable=True)
    last_name: str = Column(String(100), nullable=True)
    hashed_password: str = Column(String(128), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow,
                                  onupdate=datetime.utcnow)
    is_active: bool = Column(Boolean, default=True)
