import jwt

from datetime import datetime, timedelta

from config import password_context, settings


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def encode_jwt(
        payload: dict,
        private_key: str = settings.PRIVATE_KEY_PATH.read_text(),
        algorithm: str = settings.ALGORITHM,
        expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
):
    to_encode = payload.copy()

    now = datetime.utcnow()
    expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=expire,
        iat=now,
    )

    encoded = jwt.encode(
        payload=to_encode, key=private_key, algorithm=algorithm)

    return encoded


def decode_jwt(token: str | bytes, publick_key: str = settings.PUBLICK_KEY_PATH.read_text(), algorithm: str = settings.ALGORITHM):
    decoded = jwt.decode(jwt=token, key=publick_key, algorithms=[algorithm])

    return decoded
