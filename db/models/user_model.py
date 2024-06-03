from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, TIMESTAMP, Enum, ForeignKey, LargeBinary
from config.config import Role

metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column("id", Integer, unique=True, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("surname", String(100), nullable=False),
    Column("email", String(100), nullable=False, unique=True),
    Column("password", LargeBinary, nullable=False),
    Column("avatar_url", String()),
    Column("role", Enum(Role), nullable=False, default=Role.student.name),
    Column("is_active", Boolean, nullable=False, default=True)
)