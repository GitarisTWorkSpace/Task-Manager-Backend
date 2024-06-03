from pydantic import BaseModel, EmailStr

class UserChangePassword(BaseModel):
    password: str

class UserChangeInfo(BaseModel):
    name: str
    surname: str
    email: EmailStr
    role: str
    is_active: bool

class RoleInfo(BaseModel):
    name: str
    super_user: bool
    can_create_template: bool
    can_assing_mentors: bool
    