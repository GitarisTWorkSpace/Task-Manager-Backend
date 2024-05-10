from typing import List
from pydantic import BaseModel, EmailStr
from datetime import datetime
from auth.schemas.schemas import UserInfo

class AddStatus(BaseModel):
    project_id: int
    status_name: str   

class StatusInfo(BaseModel):
    index: int
    project_id: int
    status_name: str

class AddProject(BaseModel):
    title: str
    description: str
    columens: List[AddStatus]
    mentors: List[UserInfo]
    students: List[UserInfo]

class ProjectInfo(BaseModel):
    index: int
    title: str
    description: str
    create_at: datetime
    columens: List[StatusInfo]
    mentors: List[UserInfo]
    students: List[UserInfo]

class AddTask(BaseModel):
    title: str
    description: str
    date_start: datetime 
    date_finish: datetime 
    status: StatusInfo
    assessment: int
    student: UserInfo # EmailStr
    mentor: UserInfo

class TaskInfo(BaseModel):
    index: int
    project: int
    title: str
    description: str 
    create_at: datetime
    date_start: datetime 
    date_finish: datetime 
    assessment: int 
    status: StatusInfo
    mentor: UserInfo
    student: UserInfo