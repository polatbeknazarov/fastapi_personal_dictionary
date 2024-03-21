from typing import Optional
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str
    password2: str


class Token(BaseModel):
    access_token: str
    token_type: str
