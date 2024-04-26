from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy import MetaData, Table, Column, Integer, String, Enum
import enum 

metadata = MetaData()

class ProfileType(enum.Enum):
    student = "Стажер"
    mentor = "Наставник"

user = Table(
    "user",
    metadata,
    Column("id", Integer, unique=True, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("surname", String(50), nullable=False),
    Column("email", String(60), nullable=False),
    Column("hash_password", String, nullable=False),
    Column("profile_type", Enum(ProfileType), default=ProfileType.student, nullable=False)
)

# class UserModels(Base):
#     __tablename__ = "User"

#     id = Column(Integer, unique=True, primary_key=True)
#     name = Column(String(50))
#     surname = Column(String(50))
#     email = Column(String(50))
#     hash_password = Column(String)
#     profile_tupe = Column(Enum(ProfileType))


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True
    
