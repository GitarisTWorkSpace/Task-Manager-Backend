from pydantic import BaseModel, EmailStr

class NewPassword(BaseModel):
    old_password: str
    new_password: str

class UserChangeInfo(BaseModel):
    name: str
    surname: str
    email: EmailStr