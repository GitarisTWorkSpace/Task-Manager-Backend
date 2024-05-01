from pydantic import BaseModel
from datetime import datetime

class ProjectInfo(BaseModel):
    index: int
    title: str
    description: str
    create_at: datetime
    mentors: list
    students: list