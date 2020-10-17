from typing import Optional, List

import uuid as uuid
from pydantic import BaseModel


class User(BaseModel):
    name: str
    list_comment: list


class Commenter(BaseModel):
    name: str
    id: str


class NewComment(BaseModel):
    body: str
    rating: int = None
    domain: str
    route: str


class NewReply(BaseModel):
    list_parent: List[str]
    body: str
    rating: int = None
    domain: str
    route: str


class UpdateComment(BaseModel):
    body: Optional[str]
    id = str
    rating: Optional[int]
    domain: str
    route: str


class DeleteComment(BaseModel):
    list_id: List[str]
    domain: str
    route: str


class SignInEmailPassword(BaseModel):
    email: str
    password: str

