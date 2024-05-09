from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.sesion import get_async_session
from auth.models.models import ProfileType
from tasks.models.models import project as Project, status as Status, user_in_project as User_Project
from auth.schemas.schemas import UserInfo
import tasks.utils.utils as task_utils 
import auth.utils.utils_jwt as auth_utils
import tasks.schemas.schemas as task_schemas

router = APIRouter(prefix="/task", tags=["Tasks"])

@router.get("/{project_id}/all")
async def get_all_tasks_in_project(
    project_id: int,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> List[task_schemas.TaskInfo]:
    
    this_project = await task_utils.get_project_information_by_index(session, project_id)
    if this_project == None: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

@router.get("/{project_id}/{task_id}")
async def get_infornation_about_task(
    task_id: int,
    project_id: int,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> task_schemas.TaskInfo:
    pass

@router.post("/{project_id}/add")
async def add_task_in_project(
    project_id: int,
    task_info: task_schemas.AddTask,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> task_schemas.TaskInfo:
    pass

@router.put("/{project_id}/{task_id}")
async def change_information_about_task(
    task_id: int,
    project_id: int,
    task_info: task_schemas.AddTask,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> task_schemas.TaskInfo:
    pass

@router.delete("/{project_id}/{task_id}")
async def delete_task(
    task_id: int,
    project_id: int,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)):
    pass