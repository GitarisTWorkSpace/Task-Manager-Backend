from fastapi import APIRouter, Depends, HTTPException, status, File
from typing import List
from db.sesion import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from auth.utils.utils import get_current_token_payload
from admin.schemas.shemas import RoleInfo

role_router = APIRouter(prefix="/role", tags=["Admin_Role"])

@role_router.get("/all",
                 response_model=List[RoleInfo])
def get_all_roles(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    #check permissions
    #return list of roles
    pass

@role_router.get("/{id}")
def get_info_about_role(
    id: int,
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    #check permissions
    pass