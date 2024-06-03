from fastapi import APIRouter, Depends, HTTPException, status
from db.sesion import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from auth.utils.utils import get_current_token_payload
from auth.schemas.schemas import UserInfo, UserRegistration, UserLogin, TokensInfo

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/registration",
                 response_model=UserInfo)
def registration_user(
    user_reg_info: UserRegistration,
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
): 
    # check permissions
    # Create dict whit user info
    # Add user info in bd
    # Return user info from bd # by Email
    pass

@auth_router.post("/login",
                  response_model=TokensInfo)
def login_valid_user(
    user_login_info: UserLogin,
    session: AsyncSession = Depends(get_async_session)
):
    #check user in bd # if user not exist in bd raise exception else 
    #check user is active # if not raise exception else 
    #check valid password 
    #return access token and refresh token
    pass

@auth_router.get("/refresh",
                 response_class=TokensInfo,
                 response_model_exclude_none=True)
def create_new_access_token_by_refresh(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    #check user in bd # if user not exist in bd raise exception else 
    #check user is active # if not raise exception else 
    #return new access token and current refresh token
    pass