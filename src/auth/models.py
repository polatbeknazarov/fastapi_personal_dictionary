from sqlalchemy import Column, String


from database import Base


class User(Base):
    username: str = Column(String(50), unique=True, nullable=False)
    first_name: str = Column(String(100), nullable=True)
    last_name: str = Column(String(100), nullable=True)
    email: str = Column(String(100), nullable=False, unique=True)
    hashed_password: str = Column(String(128), nullable=False)
