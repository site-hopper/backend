import uuid as uuid
from pydantic import BaseModel
from typing import List


class Vote(BaseModel):
    up: bool
    list_parent: List[uuid.UUID]
    domain: str
    route: str


class RemoveVote(BaseModel):
    list_parent: List[uuid.UUID]
    domain: str
    route: str
