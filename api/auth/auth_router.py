from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from config.config import settings
from db.sesion import get_async_session
from db.utils import utils_user
from api.auth.utils import utils_login, utils_jwt
from api.auth.schemas.schemas import UserInfo, UserRegistration, TokenInfo

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/registration", response_model=UserInfo)
async def user_registration(
    user: UserRegistration,
    session: AsyncSession = Depends(get_async_session)
):
    user_in_db = await utils_user.get_current_user_by_email(session, user.email)

    if user_in_db:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists"
        )
    
    return await utils_user.add_user_in_db(user, session)

@auth_router.post("/login", response_model=TokenInfo)
async def auth_user_issue_jwt(
    user: UserInfo = Depends(utils_login.validate_auth_user)
):
    access_token = utils_login.create_access_token(user)
    refresh_token = utils_login.create_refresh_token(user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )

@auth_router.get("/refresh", response_model=TokenInfo)
async def auth_refresh_jwt(
    payload: dict = Depends(utils_jwt.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    token_type = payload.get(settings.token_info.TOKEN_TYPE_FIELD)
    if token_type != settings.token_info.REFRESH_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invatid token type {token_type!r} expected {settings.token_info.REFRESH_TOKEN_TYPE!r}"
        )

    user_in_db = await utils_user.get_current_user_by_index(session, payload.get("sub"))
    user_in_db = utils_user.user_in_db_transform_in_user_info(user_in_db)

    access_token = utils_login.create_access_token(user_in_db)
    refresh_token = utils_login.create_refresh_token(user_in_db)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )