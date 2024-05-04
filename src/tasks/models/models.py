from sqlalchemy import MetaData, Table, Column, Integer, String, Enum, DateTime, ForeignKey
from auth.models.models import user
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
    Column("user", ForeignKey(user.c.id, ondelete="CASCADE"), primary_key=True),
    Column("project", ForeignKey("project.id", ondelete="CASCADE"), primary_key=True)
)

status = Table(
    "status",
    metadata,
    Column("id", Integer, unique=True, primary_key=True),
    Column("project", ForeignKey("project.id", ondelete="CASCADE"), nullable=False, ),
    Column("status_name", String(50), nullable=False)
)

task = Table(
    "task",
    metadata,
    Column("id", Integer, unique=True, primary_key=True),
    Column("project", ForeignKey("project.id", ondelete="CASCADE")),
    Column("title", String(150), nullable=False),
    Column("description", String(300)),
    Column("create_at", DateTime, default=datetime.utcnow, nullable=False),
    Column("date_start", DateTime),
    Column("date_finish", DateTime),
    Column("assessment", Integer),
    Column("status", ForeignKey("status.id"), nullable=False),
    Column("mentor", ForeignKey(user.c.id, ondelete="SET NULL"), nullable=False),
    Column("student", ForeignKey(user.c.id, ondelete="SET NULL"))
)
