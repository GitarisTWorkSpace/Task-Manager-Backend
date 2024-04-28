from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from auth.models.models import user as UserModel
from auth.schemas.schemas import UserInfo

async def get_current_user_by_email(
    session: AsyncSession,
    user_email: EmailStr) -> dict:
    query = select(UserModel).where(UserModel.c.email == user_email)
    user = await session.execute(query)
    result = user.mappings().all()
    if len(result) > 0:
        return result[0]
    else :
        return None
    
async def get_current_user_by_index(
    session: AsyncSession,
    user_id: int) -> dict:
    query = select(UserModel).where(UserModel.c.id == user_id)
    user = await session.execute(query)
    result = user.mappings().all()
    if len(result) > 0:
        return result[0]
    else :
        return None