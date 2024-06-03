from fastapi import HTTPException, status, Depends
from datetime import timedelta
from db.utils.utils_user import get_current_user_by_email
from sqlalchemy.ext.asyncio import AsyncSession
from db.sesion import get_async_session
from api.auth.utils import utils_password, utils_jwt
from api.auth.schemas.schemas import LoginUserData, UserInfo
from config.config import settings

def create_access_token(user: UserInfo):
    jwt_payload: dict = {
        "sub": user.index,
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "role": user.role.name,
        "is_active": user.is_active  
    }

    return utils_jwt.create_jwt_token(
        token_type=settings.token_info.ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes
    )

def create_refresh_token(user: UserInfo):
    jwt_payload: dict = {
        "sub": user.index
    }

    return utils_jwt.create_jwt_token(
        token_type=settings.token_info.REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days)
    )

async def validate_auth_user(
    user_login: LoginUserData,
    session: AsyncSession = Depends(get_async_session)
) -> UserInfo:
    unauthed_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid login or password"
    )

    user_in_db = await get_current_user_by_email(session, user_login.email)

    if user_in_db == None:
        raise unauthed_exp
    
    if not utils_password.validate_password(
        password=user_login.password,
        hashed_password=user_in_db.get("password")
    ):
        raise unauthed_exp
    
    return UserInfo(
        index=user_in_db.get("id"),
        name=user_in_db.get("name"),
        surname=user_in_db.get("surname"),
        email=user_in_db.get("email"),
        avatar_url=user_in_db.get("avatar_url"),
        role=user_in_db.get("role"),
        is_active=user_in_db.get("is_active")
    )
    
    