from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.sesion import get_async_session
import utils.utils as pj_utils 
import schemas.schemas as task_schemas

router = APIRouter(prefix="/project")

@router.get("/project/{project_id}")
async def get_information_about_project(
    project_id: int,
    payload: dict = Depends(pj_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> task_schemas.ProjectInfo:
    pass

@router.post("/project/add")
async def add_informaion_about_project(
    project_info: task_schemas.ProjectInfo,
    payload: dict = Depends(pj_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> task_schemas.ProjectInfo:
    pass

@router.put("/project/{project_id}")
async def change_information_about_project(
    project_id: int,
    payload: dict = Depends(pj_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> task_schemas.ProjectInfo:
    pass

@router.delete("/project/{project_id}")
async def delete_project(
    project_id: int,
    payload: dict = Depends(pj_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)):
    pass
