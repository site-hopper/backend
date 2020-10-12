from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl


class UserInLogin(BaseModel):
    email: EmailStr
    password: str


class UserInCreate(BaseModel):
    email: EmailStr
    password: str
    display_name: str


class UserInUpdate(UserInCreate):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserWithToken:
    token: str


class UserInResponse:
    def __init__(self, token):
        print(type(token))
        self.token = token
    token: str
