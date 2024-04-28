from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from db.sesion import get_async_session
from pydantic import EmailStr
from typing import Annotated
from auth.models.models import user as UserModel
import auth.schemas.schemas as schemas
import auth.utils.utils_db as db_utils
import auth.utils.utils_jwt as auth_utils

router = APIRouter(prefix="/jwt", tags=["Auth"])

async def check_exists_user(
    user: schemas.UserRegistration,
    session: AsyncSession = Depends(get_async_session)) -> schemas.UserRegistration:
    
    user_db = await db_utils.get_current_user_by_email(session, user.email)
    if user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User already exists"
        )
    
    return user 

@router.post("/registration/", response_model=schemas.UserInfo)
async def registration_user(
    user: schemas.UserRegistration = Depends(check_exists_user),
    session: AsyncSession = Depends(get_async_session)) -> schemas.UserInfo:

    new_user: dict = {
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "profile_type": user.profile_type,
        "hash_password": auth_utils.hash_password(user.password)
    }

    stmt = insert(UserModel).values(new_user)
    await session.execute(stmt)
    await session.commit()

    user_db = await db_utils.get_current_user_by_email(session, user.email)

    return schemas.UserInfo(
        index=user_db.get("id"),
        name=user_db.get("name"),
        surname=user_db.get("surname"),
        email=user_db.get("email"),
        profile_type=user_db.get("profile_type"),
        is_active=user_db.get("is_active")
    )

async def validate_auth_user(
    # email: Annotated[EmailStr, Form()],
    # password: Annotated[str, Form()],
    email: EmailStr,
    password: str,
    session: AsyncSession = Depends(get_async_session)):

    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password"
    )

    user_db = await db_utils.get_current_user_by_email(session, email)

    if not user_db:
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=password,
        hashed_password=user_db.get("hash_password")
    ):
        raise unauthed_exc
    
    if not user_db.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive"
        )

    return schemas.UserInfo(
        index=user_db.get("id"),
        name=user_db.get("name"),
        surname=user_db.get("surname"),
        email=user_db.get("email"),
        profile_type=user_db.get("profile_type"),
        is_active=user_db.get("is_active")
    )
    
    

@router.post("/login/", response_model=schemas.TokenInfo)
def auth_user_issue_jwt(user: schemas.UserInfo = Depends(validate_auth_user)) -> schemas.TokenInfo:
    
    jwt_payload: dict = {
        "sub": user.index,
        "name": user.name,
        "surname":user.surname,
        "email": user.email,
        "profile_type": user.profile_type.name,
        "is_active": user.is_active
    }

    accesss_token = auth_utils.encode_jwt(jwt_payload)

    return schemas.TokenInfo(
        access_token=accesss_token,
        token_type="Bearer"
    )