from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from db.sesion import get_async_session
from pydantic import EmailStr
from typing import Annotated
from auth.models.models import user as UserModel
import auth.schemas.schemas as schemas
import auth.utils.utils_jwt as auth_utils

http_bearer = HTTPBearer()

router = APIRouter(prefix="/jwt", tags=["Auth"])

async def check_exists_user(
    user: schemas.UserRegistration,
    session: AsyncSession = Depends(get_async_session)
) -> schemas.UserRegistration:
    query = select(UserModel).where(UserModel.c.email == user.email)
    result = await session.execute(query)
    if result.all():
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

    query = select(UserModel).where(UserModel.c.email == user.email)
    result = await session.execute(query)
    user_info: dict = result.mappings().all()[0]
    return schemas.UserInfo(
        index=user_info.get("id"),
        name=user_info.get("name"),
        surname=user_info.get("surname"),
        email=user_info.get("email"),
        profile_type=user_info.get("profile_type"),
        is_active=user_info.get("is_active")
    )

async def validate_auth_user(
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    session: AsyncSession = Depends(get_async_session)
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password"
    )
    query = select(UserModel).where(UserModel.c.email == email)
    check_user = await session.execute(query)
    # print(check_user.mappings().all())

    user_info: dict = check_user.mappings().all()[0]

    if not user_info:
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=password,
        hashed_password=user_info.get("hash_password")
    ):
        raise unauthed_exc
    
    if not user_info.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive"
        )

    return schemas.UserInfo(
        index=user_info.get("id"),
        name=user_info.get("name"),
        surname=user_info.get("surname"),
        email=user_info.get("email"),
        profile_type=user_info.get("profile_type"),
        is_active=user_info.get("is_active")
    )
    
    

@router.post("/login/", response_model=schemas.TokenInfo)
def auth_user_issue_jwt(user: schemas.UserInfo = Depends(validate_auth_user)) -> schemas.TokenInfo:
    print(user)
    # jwt_payload = {
    #     "sub": user.index,
    #     "name": user.name,
    #     "email": user.email,
    #     "profile_type": user.profile_type,
    # }

    jwt_payload = {
        "sub": user.index,
        "name": user.name,
        "surname":user.surname,
        "email": user.email,
        "profile_type": user.profile_type,
        "is_active": user.is_active
    }

    # accesss_token = "sdjgisdbgjsnd.dsnfsndsjdn.sdnsuidgbduvn"

    accesss_token = auth_utils.encode_jwt(jwt_payload)

    return schemas.TokenInfo(
        access_token=accesss_token,
        token_type="Bearer"
    )

def get_current_token_payload(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) :
    token = credentials.credentials
    try:
        payload = auth_utils.decoded_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token error"
        )
    
    return payload

async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> schemas.UserInfo:

    query = select(UserModel).where(UserModel.c.email == payload.get("email"))
    check_user = await session.execute(query)

    user_info: dict = check_user.mappings().all()[0]

    if user_info:
        return schemas.UserInfo(
            index=user_info.get("id"),
            name=user_info.get("name"),
            surname=user_info.get("surname"),
            email=user_info.get("email"),
            profile_type=user_info.get("profile_type"),
            is_active=user_info.get("is_active")
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
def auth_user_check_self_info(user: schemas.UserInfo = Depends(get_current_active_auth_user)):
    return user