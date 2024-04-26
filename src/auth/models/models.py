from sqlalchemy import MetaData, Table, Column, Integer, String, Enum, BINARY
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