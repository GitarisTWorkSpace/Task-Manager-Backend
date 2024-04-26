from pydantic import BaseModel, EmailStr
from db.models.models import ProfileType

class TokenInfo(BaseModel):
    access_token: str
    token_type: str

class UserInfo(BaseModel):
    index: int
    name: str
    surname: str
    email: EmailStr
    profile_type: ProfileType

class UserRegistration(UserInfo):
    password: str