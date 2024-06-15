from sqlalchemy import MetaData, Table, Column, ForeignKey
from db.models.user_model import user as UserModel

metadata = MetaData()

connection = Table(
    "connection",
    metadata,
    Column("student", ForeignKey(UserModel.c.id, ondelete="CASCADE"), nullable=False, primary_key=True),
    Column("mentor", ForeignKey(UserModel.c.id, ondelete="CASCADE"), nullable=False)
)