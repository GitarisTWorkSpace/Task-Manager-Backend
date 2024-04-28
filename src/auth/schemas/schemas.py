from pydantic import BaseModel, EmailStr
from auth.models.models import ProfileType

class TokenInfo(BaseModel):
    access_token: str
    token_type: str

class UserInfo(BaseModel):
    index: int 
    name: str
    surname: str
    email: EmailStr
    profile_type: ProfileType = ProfileType.student
    is_active: bool

class UserRegistration(BaseModel):
    name: str
    surname: str
    email: EmailStr
    profile_type: ProfileType = ProfileType.student
    password: str
