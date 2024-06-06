from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db.utils import utils_user

async def check_user_in_db(
    user_id: int,
    session: AsyncSession
):
    #check user in bd # if user not exist in bd raise exception else 
    user_in_db = await utils_user.get_current_user_by_index(session, user_id)
    if user_in_db == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return await check_user_is_active(user_in_db)

async def check_user_is_active(
    user_info: dict,
):
    if user_info.get("is_active") == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive"
        )
    
    return user_info