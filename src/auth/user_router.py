from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from db.sesion import get_async_session
from pydantic import EmailStr
from typing import Annotated
from auth.models.models import user as UserModel
from auth.models.models import ProfileType
import auth.schemas.schemas as schemas
import auth.utils.utils_db as db_utils
import auth.utils.utils_jwt as auth_utils

http_bearer = HTTPBearer()

router = APIRouter(prefix="/user", tags=["Auth"])

async def get_current_auth_user(
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> schemas.UserInfo:

    user_db = await db_utils.get_current_user_by_email(session, payload.get("email"))

    if user_db:
        return schemas.UserInfo(
            index=user_db.get("id"),
            name=user_db.get("name"),
            surname=user_db.get("surname"),
            email=user_db.get("email"),
            profile_type=user_db.get("profile_type"),
            is_active=user_db.get("is_active")
        )
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid"
    )

def get_current_active_auth_user(user: schemas.UserInfo = Depends(get_current_auth_user)):
    if user.is_active:
        return user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User inactive"
    )

@router.get("/me")
def auth_user_check_self_info(user: schemas.UserInfo = Depends(get_current_active_auth_user)) -> schemas.UserInfo:
    return user

@router.get("/{user_id}")
async def get_information_about_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
    ) -> schemas.UserInfo: 

    user = await db_utils.get_current_user_by_index(session, user_id)

    return schemas.UserInfo(
        index=user.get("id"),
        name=user.get("name"),
        surname=user.get("surname"),
        email=user.get("email"),
        profile_type=user.get("profile_type"),
        is_active=user.get("is_active")
    )

@router.post("/me")
async def change_user_password(
    old_password: str,
    new_password: str,
    session: AsyncSession = Depends(get_async_session),
    payload: dict = Depends(auth_utils.get_current_token_payload)) -> schemas.UserInfo:
    
    user_db = await db_utils.get_current_user_by_email(session, payload.get("email"))

    print(user_db)

    if not auth_utils.validate_password(
        password=old_password,
        hashed_password=user_db.get("hash_password")
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password change error"
        )
    
    new_hash_password = auth_utils.hash_password(new_password)

    stmt = update(UserModel).where(UserModel.c.id == user_db.get("id")).values(hash_password=new_hash_password)
    await session.execute(stmt)
    await session.commit()

    return schemas.UserInfo(
        index=user_db.get("id"),
        name=user_db.get("name"),
        surname=user_db.get("surname"),
        email=user_db.get("email"),
        profile_type=user_db.get("profile_type"),
        is_active=user_db.get("is_active")
    )

@router.put("/me")
async def change_information_about_user(
    new_info_about_user: schemas.UserInfo, 
    session: AsyncSession = Depends(get_async_session),
    payload: dict = Depends(auth_utils.get_current_token_payload)) -> schemas.UserInfo:
    
    user_db = await db_utils.get_current_user_by_email(session, payload.get("email"))

    print(user_db)

    if new_info_about_user.name != user_db.get("name"):
        stmt = update(UserModel).where(UserModel.c.id == user_db.get("id")).values(name=new_info_about_user.name)
        await session.execute(stmt)
        await session.commit()
    
    if new_info_about_user.surname != user_db.get("surname"):
        stmt = update(UserModel).where(UserModel.c.id == user_db.get("id")).values(surname=new_info_about_user.surname)
        await session.execute(stmt)
        await session.commit()
    
    if new_info_about_user.email != user_db.get("email"):
        stmt = update(UserModel).where(UserModel.c.id == user_db.get("id")).values(email=new_info_about_user.email)
        await session.execute(stmt)
        await session.commit()  

    new_user_info = await db_utils.get_current_user_by_index(session, user_db.get("id"))

    return schemas.UserInfo(
        index=new_user_info.get("id"),
        name=new_user_info.get("name"),
        surname=new_user_info.get("surname"),
        email=new_user_info.get("email"),
        profile_type=new_user_info.get("profile_type"),
        is_active=new_user_info.get("is_active")
    )

@router.delete("/me")
async def delete_user_account(
    session: AsyncSession = Depends(get_async_session),
    payload: dict = Depends(auth_utils.get_current_token_payload)):
    
    user_db = await db_utils.get_current_user_by_email(session, payload.get("email"))

    print(user_db)

    stmt = delete(UserModel).where(UserModel.c.id == user_db.get("id"))
    await session.execute(stmt)
    await session.commit()  

    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail="User deleted"
    )
