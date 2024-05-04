from typing import List
from pydantic import BaseModel, EmailStr
from datetime import datetime
from auth.schemas.schemas import UserInfo

class StatusInfo(BaseModel):
    project_id: int
    status_name: str

class AddProject(BaseModel):
    title: str
    description: str
    columens: List[StatusInfo]
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

class AllStatusInProjectInfo(BaseModel):
    project_index: int
    project_title: str
    status_name: List[str]

class AddTask(BaseModel):
    project_id: int
    title: str
    description: str
    date_start: datetime 
    date_finish: datetime 
    status: str
    student_email: EmailStr 

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