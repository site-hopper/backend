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
    commenter: Commenter


class NewReply(BaseModel):
    list_parent: List[uuid.UUID]
    body: str
    rating: int = None
    domain: str
    route: str
    commenter: Commenter


class UpdateComment(BaseModel):
    body: Optional[str]
    id = str
    rating: Optional[int]
    domain: str
    route: str

