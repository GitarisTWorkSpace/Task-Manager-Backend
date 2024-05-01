from sqlalchemy import MetaData, Table, Column, Integer, String, Enum, LargeBinary, Boolean, DateTime, ForeignKey
from src.auth.models.models import user
from datetime import datetime

metadata = MetaData()

project = Table(
    "project",
    metadata,
    Column("id", Integer, unique=True, primary_key=True),
    Column("title", String(150), nullable=False),
    Column("description", String(300)),
    Column("create_at", DateTime, default=datetime.utcnow, nullable=False)
)

user_in_project = Table(
    "user_in_project",
    metadata,
    Column("user", ForeignKey(user.c.id), primary_key=True),
    Column("project", ForeignKey("project.id"), primary_key=True)
)

status = Table(
    "status",
    metadata,
    Column("project", ForeignKey("project.id"), primary_key=True),
    Column("status_name", String(50), nullable=False)
)

task = Table(
    "task",
    metadata,
    Column("id", Integer, unique=True, primary_key=True),
    Column("project", ForeignKey("project.id")),
    Column("title", String(150), nullable=False),
    Column("description", String(300)),
    Column("create_at", DateTime, default=datetime.utcnow, nullable=False),
    Column("date_start", DateTime),
    Column("date_finish", DateTime),
    Column("Assessment", Integer),
    Column("status", ForeignKey("status.project"), nullable=False),
)
