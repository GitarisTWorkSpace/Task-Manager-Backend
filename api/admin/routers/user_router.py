from fastapi import APIRouter, Depends, HTTPException, status, File
from typing import List
from db.sesion import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from auth.utils.utils import get_current_token_payload
from auth.schemas.schemas import UserInfo 
from admin.schemas.shemas import UserChangePassword, UserChangeInfo

admin_user_router = APIRouter(prefix="/user", tags=["Admin_User"])

@admin_user_router.get("/all",
                       response_model=List[UserInfo])
def get_info_about_all_users(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    # return all list of info user 
    pass

@admin_user_router.put("/{id}")
def change_user_info(
    id: int,
    new_user_info: UserChangeInfo,
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    #check permissions
    #check user in bd 
    #change user info in bd
    #return new user info 
    pass

@admin_user_router.post("/{id}")
def change_password_user(
    id: int,
    new_password: UserChangePassword,
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    #check permissions
    #check user in bd 
    #change user info in bd
    #return status 200
    pass

@admin_user_router.delete("/{id}")
def delete_user(
    id: int,
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    #check permissions
    #check user in bd 
    #delete user info in bd
    #return status 200
    pass