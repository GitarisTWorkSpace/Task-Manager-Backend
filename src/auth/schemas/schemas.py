from pydantic import BaseModel, EmailStr, FileUrl

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInfo(BaseModel):
    index: int
    name: str
    surname: str
    email: EmailStr
    avatarUrl: str | None = None #FileUrl
    role: str
    is_active: bool

class UserRegistration(BaseModel):
    name: str
    surname: str
    email: EmailStr
    role: str
    password: str

class TokensInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"