from pydantic import BaseModel, EmailStr, ConfigDict

class UserModel(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True

