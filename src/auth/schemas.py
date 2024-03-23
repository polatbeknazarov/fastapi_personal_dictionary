from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    username: Optional[str]
    password: str


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str = Field(min_length=7, max_length=128)
    password2: str = Field(min_length=7, max_length=128)


class UserRead(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
