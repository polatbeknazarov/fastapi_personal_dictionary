from pathlib import Path
from pydantic_settings import BaseSettings
from passlib.context import CryptContext


BASE_DIR = Path(__file__).parent.parent


password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Settings(BaseSettings):
    # Database Settings
    db_url: str = f'sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3'
    db_echo: bool = True

    # JWT Settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM: str = 'RS256'
    PRIVATE_KEY_PATH: Path = BASE_DIR / 'private.pem'
    PUBLICK_KEY_PATH: Path = BASE_DIR / 'publick.pem'


settings = Settings()
