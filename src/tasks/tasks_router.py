from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.sesion import get_async_session
import tasks.utils.utils as task_utils 
import auth.utils.utils_jwt as auth_utils
import tasks.schemas.schemas as task_schemas

router = APIRouter(prefix="/task", tags=["Tasks"])

@router.get("/{project_id}/all")
async def get_all_tasks_in_project(
    project_id: int,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> List[task_schemas.TaskInfo]:
    pass 

@router.get("/{project_id}/{task_id}")
async def get_infornation_about_task(
    task_id: int,
    project_id: int,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> task_schemas.TaskInfo:
    pass

@router.post("/{project_id}/add")
async def add_task_in_project(
    task_id: int,
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
    session: AsyncSession = Depends(get_async_session)) -> task_schemas.TaskInfo:
    pass