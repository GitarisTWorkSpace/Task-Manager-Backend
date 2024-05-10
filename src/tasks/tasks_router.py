from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.sesion import get_async_session
from auth.models.models import ProfileType
from tasks.models.models import project as Project, status as Status, user_in_project as User_Project, task as Task
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
    
    if not await task_utils.check_user_in_project(session, payload.get("sub"), project_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of this project"
        )
    
    query = select(Task).where(Task.c.project == project_id)
    result = await session.execute(query)
    result_list = result.mappings().all()

    if len(result_list) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task list empty"
        )

    task_list: List[task_schemas.TaskInfo] = []

    for i in range(len(result_list)):
        task_list.append(
            await task_utils.get_information_about_task(session, project_id, result_list[i].get("id"))
        )

    return task_list
    
@router.get("/{project_id}/{task_id}")
async def get_infornation_about_task(
    task_id: int,
    project_id: int,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> task_schemas.TaskInfo:

    this_project = await task_utils.get_project_information_by_index(session, project_id)
    if this_project == None: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if not await task_utils.check_user_in_project(session, payload.get("sub"), project_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of this project"
        )
    
    return await task_utils.get_information_about_task(session, project_id, task_id)

@router.post("/{project_id}/add")
async def add_task_in_project(
    project_id: int,
    task_info: task_schemas.AddTask,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> task_schemas.TaskInfo:

    if payload.get("profile_type") != ProfileType.mentor.name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )

    this_project = await task_utils.get_project_information_by_index(session, project_id)
    if this_project == None: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if not await task_utils.check_user_in_project(session, payload.get("sub"), project_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of this project"
        )
    
    new_task: dict = {
        "project": project_id,
        "title": task_info.title,
        "description": task_info.description,
        "date_start": task_info.date_start,
        "date_finish": task_info.date_finish,
        "assessment": task_info.assessment,
        "status": task_info.status.index,
        "mentor": task_info.mentor.index,
        "student": task_info.student.index
    }

    stmt = insert(Task).values(new_task)
    await session.execute(stmt)
    await session.commit()

    query = select(Task).where(
        Task.c.title == task_info.title,
        Task.c.description == task_info.description,
        Task.c.project == project_id,
        Task.c.assessment == task_info.assessment
    )
    result = await session.execute(query)
    result_list = result.mappings().all()

    if len(result_list) > 0:
        this_task: dict = result_list[0]
    
    return await task_utils.get_information_about_task(session, project_id, this_task.get("id"))

@router.put("/{project_id}/{task_id}")
async def change_information_about_task(
    task_id: int,
    project_id: int,
    task_info: task_schemas.AddTask,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> task_schemas.TaskInfo:

    this_project = await task_utils.get_project_information_by_index(session, project_id)
    if this_project == None: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if not await task_utils.check_user_in_project(session, payload.get("sub"), project_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of this project"
        )
    
    task_in_db = await task_utils.get_information_about_task(session, project_id, task_id)

    if task_info.status.index != task_in_db.status.index:
            stmt = update(Task).where(
                Task.c.id == task_id,
                Task.c.project == project_id).values(
                    status=task_info.status.index)
            await session.execute(stmt)
            await session.commit() 

    if payload.get("profile_type") == ProfileType.mentor.name:

        if task_info.title != task_in_db.title:
            stmt = update(Task).where(
                Task.c.id == task_id,
                Task.c.project == project_id).values(
                    title=task_info.title)
            await session.execute(stmt)
            await session.commit()

        if task_info.description != task_in_db.description:
            stmt = update(Task).where(
                Task.c.id == task_id,
                Task.c.project == project_id).values(
                    description=task_info.description)
            await session.execute(stmt)
            await session.commit()
        
        if task_info.date_start != task_in_db.date_start:
            stmt = update(Task).where(
                Task.c.id == task_id,
                Task.c.project == project_id).values(
                    date_start=task_info.date_start)
            await session.execute(stmt)
            await session.commit()

        if task_info.date_finish != task_in_db.date_finish:
            stmt = update(Task).where(
                Task.c.id == task_id,
                Task.c.project == project_id).values(
                    date_finish=task_info.date_finish)
            await session.execute(stmt)
            await session.commit() 

        if task_info.assessment != task_in_db.assessment:
            stmt = update(Task).where(
                Task.c.id == task_id,
                Task.c.project == project_id).values(
                    assessment=task_info.assessment)
            await session.execute(stmt)
            await session.commit() 

        if task_info.mentor.index != task_in_db.mentor.index:
            stmt = update(Task).where(
                Task.c.id == task_id,
                Task.c.project == project_id).values(
                    mentor=task_info.mentor.index)
            await session.execute(stmt)
            await session.commit() 

        if task_info.student.index != task_in_db.student.index:
            stmt = update(Task).where(
                Task.c.id == task_id,
                Task.c.project == project_id).values(
                    student=task_info.student.index)
            await session.execute(stmt)
            await session.commit() 

    return await get_infornation_about_task(session, project_id, task_id)

@router.delete("/{project_id}/{task_id}")
async def delete_task(
    task_id: int,
    project_id: int,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)):
    
    if payload.get("profile_type") != ProfileType.mentor.name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )

    this_project = await task_utils.get_project_information_by_index(session, project_id)
    if this_project == None: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if not await task_utils.check_user_in_project(session, payload.get("sub"), project_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of this project"
        )
    
    stmt = delete(Task).where(Task.c.id == task_id, Task.c.project == project_id)
    await session.execute(stmt)
    await session.commit()

    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Task deleted"
    )
    
