from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from api.auth.utils import utils_password
from api.auth.schemas.schemas import UserRegistration, UserInfo
from api.user.schemas.schemas import UserChangeInfo
from db.models.user_model import user as UserModel

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

def user_in_db_transform_in_user_info(user_in_db: dict) -> UserInfo:
    return UserInfo(
        index=user_in_db.get("id"),
        name=user_in_db.get("name"),
        surname=user_in_db.get("surname"),
        email=user_in_db.get("email"),
        avatar_url=user_in_db.get("avatar_url"),
        role=user_in_db.get("role"),
        is_active=user_in_db.get("is_active")
    )

async def add_user_in_db(
    user: UserRegistration,
    session: AsyncSession
):
    new_user: dict = {
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "password": utils_password.hash_password(user.password),
        "role": user.role.name
    }

    stmt = insert(UserModel).values(new_user)
    await session.execute(stmt)
    await session.commit()

    user_in_db = await get_current_user_by_email(session, user.email)

    return user_in_db_transform_in_user_info(user_in_db)

async def change_user_password(
    new_password: bytes,
    user_id: int,
    session: AsyncSession
) -> bool:
    try: 
        stmt = update(UserModel).where(UserModel.c.id == user_id).values(password=new_password)
        await session.execute(stmt)
        await session.commit()
    except:
        return False
    
    return True

async def change_user_info(
    new_user_info: UserChangeInfo,
    user_id: int,
    session: AsyncSession
) -> UserInfo: 
    
    user_in_db = await get_current_user_by_index(session, user_id)

    if new_user_info.name != user_in_db.get("name"):
        stmt = update(UserModel).where(UserModel.c.id == user_id).values(name=new_user_info.name)
        await session.execute(stmt)

    if new_user_info.surname != user_in_db.get("surname"):
        stmt = update(UserModel).where(UserModel.c.id == user_id).values(surname=new_user_info.surname)
        await session.execute(stmt)
    
    if new_user_info.email != user_in_db.get("email"):
        stmt = update(UserModel).where(UserModel.c.id == user_id).values(email=new_user_info.email)
        await session.execute(stmt)

    await session.commit()

    new_user_in_db = await get_current_user_by_index(session, user_id)

    return user_in_db_transform_in_user_info(new_user_in_db)

async def delete_user(
    user_id: int,
    session: AsyncSession
) -> bool:
    try:
        stmt = delete(UserModel).where(UserModel.c.id == user_id)
        await session.execute(stmt)
        await session.commit()
    except:
        return False
    
    return True