from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings


class BaseMixin:
    id: Mapped[int] = Column(Integer, primary_key=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow,
                                  onupdate=datetime.utcnow)


class Base(DeclarativeBase, BaseMixin):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'


class DataBase:
    def __init__(self):
        self.engine = create_async_engine(
            url=settings.db_url,
            echo=settings.db_echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )


database = DataBase()
