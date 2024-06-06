from fastapi import APIRouter, Depends, HTTPException, status, File
from db.sesion import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth.utils.utils_jwt import validate_token_type_is_access
from api.auth.schemas.schemas import UserInfo 
from api.user.schemas.schemas import NewPassword, UserChangeInfo
from api.auth.utils import utils_password
from db.utils import utils_user
from api.user.utils import utils_errors

user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.get("/me", response_model=UserInfo)
async def get_information_about_me(
    payload: dict = Depends(validate_token_type_is_access),
    session: AsyncSession = Depends(get_async_session)
):
    #check user in bd # if user not exist in bd raise exception else 
    #check user is active # if not raise exception else 
    user_in_db = await utils_errors.check_user_in_db(session=session, user_id=payload.get("sub"))

    #retunr info about user
    return utils_user.user_in_db_transform_in_user_info(user_in_db)

@user_router.get("/{index}")
async def get_user_information(
    index: int,
    payload: dict = Depends(validate_token_type_is_access),
    session: AsyncSession = Depends(get_async_session)
):
    #check user in bd # if user not exist in bd raise exception else 
    user_in_db = await utils_errors.check_user_in_db(session=session, user_id=index)
    #retunr info about user
    return utils_user.user_in_db_transform_in_user_info(user_in_db)

@user_router.post("/me")
async def change_my_password(
    user_password: NewPassword,
    payload: dict = Depends(validate_token_type_is_access),
    session: AsyncSession = Depends(get_async_session)
):
    #check user in bd # if user not exist in bd raise exception else 
    #check user is active # if not raise exception else 
    user_in_db = await utils_errors.check_user_in_db(session=session, user_id=payload.get("sub"))
    #check valid old password # if not raise exception else
    if utils_password.validate_password(user_password.old_password, user_in_db.get("password")):
        #change password in db
        if await utils_user.change_user_password(utils_password.hash_password(user_password.new_password), user_in_db.get("id"), session):
            #return status 200
            return HTTPException(
                status_code=status.HTTP_200_OK,
                detail="Password changed"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Сouldn't change password"
        )
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Old password is not valid"
    )

@user_router.put("/me", response_model=UserInfo)
async def change_info_about_me(
    new_user_info: UserChangeInfo,
    payload: dict = Depends(validate_token_type_is_access),
    session: AsyncSession = Depends(get_async_session)
):
    #check user in bd # if user not exist in bd raise exception else 
    #check user is active # if not raise exception else 
    user_in_db = await utils_errors.check_user_in_db(session=session, user_id=payload.get("sub"))
    #change user info in bd
    #return new user info
    return await utils_user.change_user_info(new_user_info, user_in_db.get("id"), session)

#@user_router.put("/me/avatar")
def change_my_avatar(
    photo_file: File,
    payload: dict = Depends(validate_token_type_is_access),
    session: AsyncSession = Depends(get_async_session)
):
    #check user in bd # if user not exist in bd raise exception else 
    #check user is active # if not raise exception else 
    #change user info in bd
    #return new user info
    pass

@user_router.delete("/me")
async def delete_my_profile(
    payload: dict = Depends(validate_token_type_is_access),
    session: AsyncSession = Depends(get_async_session)
):
    #check user in bd # if user not exist in bd raise exception else 
    #check user is active # if not raise exception else 
    user_in_db = await utils_errors.check_user_in_db(session=session, user_id=payload.get("sub"))
    #delete user in db
    #return status 200
    if not await utils_user.delete_user(user_in_db.get("id"), session):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Сouldn't delete user"
        )
    
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail="User deleted successfully"
    )