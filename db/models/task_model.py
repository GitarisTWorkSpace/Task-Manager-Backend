from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, Enum, Date, JSON, ForeignKey
from datetime import datetime
from api.tasks.schemas.schemas import Status
from db.models.user_model import user as UserModel

metadata = MetaData()

task = Table(
    "task",
    metadata,
    Column("id", Integer, unique=True, primary_key=True),
    Column("title", String(150), nullable=False),
    Column("description", String()),
    Column("files", JSON),
    Column("create_at", Date, nullable=False, default=datetime.utcnow()),
    Column("start_task", Date),
    Column("finish_task", Date),
    Column("status", Enum(Status), nullable=False, default=Status.new.name),
    Column("score", Integer, nullable=False, default=0),
    Column("student", ForeignKey(UserModel.c.id, ondelete="SET NULL"), nullable=False),
    Column("mentor", ForeignKey(UserModel.c.id, ondelete="CASCADE"), nullable=False)
)