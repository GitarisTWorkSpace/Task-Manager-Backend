from typing import List
from pydantic import BaseModel, FilePath
from datetime import datetime
from api.auth.schemas.schemas import UserInfo
from enum import Enum

class Status(Enum):
    new = "Новые"
    in_work = "В работе"
    done = "Готовы"

class AddTask(BaseModel):
    title: str
    description: str | None = None
    #files_in_description_path: List[FilePath] | None = None
    start_task: datetime | None = None
    finish_task: datetime | None = None
    score: int 
    status: Status = Status.new
    student: int
    mentor: int

class TaskInfo(BaseModel):
    index: int 
    title: str
    description: str | None = None
    #files_in_description_path: List[FilePath] | None = None
    create_at: datetime
    start_task: datetime | None = None
    finish_task: datetime | None = None
    score: int 
    status: Status = Status.new
    student: int
    mentor: int



