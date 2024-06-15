from pydantic import BaseModel
from typing import List
from api.auth.schemas.schemas import UserInfo

class Connection(BaseModel):
    mentor: UserInfo
    students: List[UserInfo]

class AddConnection(BaseModel):
    mentor: int
    students: List[UserInfo]

class ChangeConection(BaseModel):
    students: List[UserInfo]