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

router = APIRouter(prefix="/project", tags=["Projects"])

@router.get("/all")
async def get_all_available_project(
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> List[task_schemas.ProjectInfo]:
    
    # Get all project id 
    query = select(User_Project).where(User_Project.c.user == payload.get("sub"))
    result = await session.execute(query)
    result_project_list = result.mappings().all()

    # If user not join in someone project, raise exception
    if len(result_project_list) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project list empty"
        )

    # Project List
    project_list: List[task_schemas.ProjectInfo] = []    
    
    for i in range(len(result_project_list)):
        project_list.append(
            await task_utils.get_information_about_project_by_index(session, result_project_list[i].get("project"))
        )

    return project_list

@router.get("/{project_id}")
async def get_information_about_project(
    project_id: int,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> task_schemas.ProjectInfo:
    
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

    return await task_utils.get_information_about_project_by_index(session, project_id)

@router.post("/add")
async def add_project(
    project_info: task_schemas.AddProject,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> task_schemas.ProjectInfo:
    
    if payload.get("profile_type") != ProfileType.mentor.name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )
    
    new_project: dict = {
        "title": project_info.title,
        "description": project_info.description
    }

    stmt = insert(Project).values(new_project)
    await session.execute(stmt)
    await session.commit()

    query = select(Project).where(
        Project.c.title == new_project.get("title"), 
        Project.c.description == new_project.get("description"))

    result = await session.execute(query)
    result_list = result.mappings().all()
    if len(result_list) > 0:
        this_project = result_list[0]
    else: 
        this_project = None

    if len(project_info.columens) >= 3:
        for i in range(len(project_info.columens)):
            new_status: dict = {
                "project": this_project.get("id"),
                "status_name": project_info.columens[i].status_name
            }
            stmt = insert(Status).values(new_status)
            await session.execute(stmt)
    else:
        status_in_new_project: List[dict] = [
            {
                "project": this_project.get("id"),
                "status_name": "Новые"
            },
            {
                "project": this_project.get("id"),
                "status_name": "В работе"
            },
            {
                "project": this_project.get("id"),
                "status_name": "Завершены"
            },
        ]

        for i in range(len(status_in_new_project)):
            stmt = insert(Status).values(status_in_new_project[i])
            await session.execute(stmt)
    await session.commit()

    if len(project_info.mentors) <= 1:
        user_in_project: dict = {
            "user": payload.get("sub"),
            "project": this_project.get("id")
        }

        stmt = insert(User_Project).values(user_in_project)
        await session.execute(stmt)
    else:
        user_in_project: dict = {
            "user": payload.get("sub"),
            "project": this_project.get("id")
        }

        stmt = insert(User_Project).values(user_in_project)
        await session.execute(stmt)

        for i in range(len(project_info.mentors)):
            if project_info.mentors[i].index == 0:
                continue
            user_in_project: dict = {
                "user": project_info.mentors[i].index,
                "project": this_project.get("id")
            }
            stmt = insert(User_Project).values(user_in_project)
            await session.execute(stmt)
    await session.commit()

    if len(project_info.students) >= 1:
        for i in range(len(project_info.students)):
            if project_info.students[i].index == 0:
                continue
            user_in_project: dict = {
            "user": project_info.students[i].index,
            "project": this_project.get("id")
            }
            stmt = insert(User_Project).values(user_in_project)
            await session.execute(stmt)
        await session.commit()

    return await task_utils.get_information_about_project_by_index(session, this_project.get("id"))

@router.put("/{project_id}")
async def change_information_about_project(
    project_id: int,
    new_project_info: task_schemas.AddProject,
    payload: dict = Depends(auth_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> task_schemas.ProjectInfo:

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

    if this_project.get("title") != new_project_info.title:
        stmt = update(Project).where(Project.c.id == project_id).values(title=new_project_info.title)
        await session.execute(stmt)
        await session.commit()
    
    if this_project.get("description") != new_project_info.description:
        stmt = update(Project).where(Project.c.id == project_id).values(description=new_project_info.description)
        await session.execute(stmt)
        await session.commit()

    columens = await task_utils.get_columens_in_project(session, project_id)

    if len(columens) != len(new_project_info.columens):
        stmt = delete(Status).where(Status.c.project == project_id)
        await session.execute(stmt)
        await session.commit()
        for i in range(len(new_project_info.columens)):
            new_status: dict = {
                "project": this_project.get("id"),
                "status_name": new_project_info.columens[i].status_name
            }
            stmt = insert(Status).values(new_status)
            await session.execute(stmt)
    else:
        for i in range(len(new_project_info.columens)):
            if columens[i].status_name != new_project_info.columens[i].status_name:
                stmt = update(Status).where(
                    Status.c.status_name == columens[i].status_name, 
                    Status.c.project == project_id).values(
                        status_name=new_project_info.columens[i].status_name)
                await session.execute(stmt)
                await session.commit()

    mentor_list: List[UserInfo] = await task_utils.metors_list_in_project(session, project_id)
    student_list: List[UserInfo] = await task_utils.students_list_in_project(session, project_id)

    for i in range(len(mentor_list)):
        stmt = delete(User_Project).where(User_Project.c.user == mentor_list[i].index)
        await session.execute(stmt)
    await session.commit()
    for i in range(len(new_project_info.mentors)):
        user_in_project: dict = {
            "user": new_project_info.mentors[i].index,
            "project": this_project.get("id")
        }
        stmt = insert(User_Project).values(user_in_project)
        await session.execute(stmt)
    await session.commit()

    for i in range(len(student_list)):
        stmt = delete(User_Project).where(User_Project.c.user == student_list[i].index)
        await session.execute(stmt)
    await session.commit()
    for i in range(len(new_project_info.students)):
        user_in_project: dict = {
            "user": new_project_info.students[i].index,
            "project": this_project.get("id")
        }
        stmt = insert(User_Project).values(user_in_project)
        await session.execute(stmt)
    await session.commit()

    return await task_utils.get_information_about_project_by_index(session, project_id)

@router.delete("/{project_id}")
async def delete_project(
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
    
    stmt = delete(Project).where(Project.c.id == project_id)
    await session.execute(stmt)
    await session.commit()

    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Project deleted"
    )
