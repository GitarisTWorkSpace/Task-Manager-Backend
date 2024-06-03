from fastapi import APIRouter, Depends, HTTPException, status, File
from db.sesion import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth.utils.utils import get_current_token_payload
from api.auth.schemas.schemas import UserInfo 
from user.schemas.schemas import NewPassword, UserChangeInfo

user_router = APIRouter(prefix="/user", tags=['User'])

@user_router.get("/me", response_model=UserInfo)
def get_information_about_me(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    #check user in bd # if user not exist in bd raise exception else 
    #check user is active # if not raise exception else 
    #retunr info about user
    pass

@user_router.get("/{id}")
def get_user_information(
    id: int,
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    #check user in bd # if user not exist in bd raise exception else 
    #retunr info about user
    pass

@user_router.post("/me")
def change_my_password(
    user_password: NewPassword,
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    #check user in bd # if user not exist in bd raise exception else 
    #check user is active # if not raise exception else 
    #check valid old password # if not raise exception else
    #change password in db
    #return status 200
    pass 

@user_router.put("/me",
                 response_model=UserInfo)
def change_info_about_me(
    new_user_info: UserChangeInfo,
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    #check user in bd # if user not exist in bd raise exception else 
    #check user is active # if not raise exception else 
    #change user info in bd
    #return new user info
    pass

@user_router.put("/me/avatar")
def change_my_avatar(
    photo_file: File,
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    #check user in bd # if user not exist in bd raise exception else 
    #check user is active # if not raise exception else 
    #change user info in bd
    #return new user info
    pass

@user_router.delete("/me")
def delete_my_profile(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    #check user in bd # if user not exist in bd raise exception else 
    #check user is active # if not raise exception else 
    #delete user in db
    #return status 200
    pass