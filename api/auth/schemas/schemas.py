from pydantic import BaseModel, EmailStr, FilePath
from config.config import Role

class UserRegistration(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    role: Role

class UserInfo(BaseModel):
    index: int
    name: str
    surname: str
    email: EmailStr
    avatar_url: FilePath | None = None #FileUrl
    role: Role = Role.student
    is_active: bool = True

class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class LoginUserData(BaseModel):
    email: EmailStr
    password: str