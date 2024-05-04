from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.sesion import get_async_session
from auth.models.models import ProfileType
from tasks.models.models import project as Project, status as Status, user_in_project as User_Project
from auth.schemas.schemas import UserInfo
import auth.utils.utils_db as db_utils
import tasks.utils.utils as tsk_utils 
import tasks.schemas.schemas as task_schemas

router = APIRouter(prefix="/project", tags=["Projects"])

@router.get("/all")
async def get_all_available_project(
    payload: dict = Depends(tsk_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> List[task_schemas.ProjectInfo]:
    
    query = select(User_Project).where(User_Project.c.user == payload.get("sub"))
    result = await session.execute(query)
    result_project_list = result.mappings().all()

    project_list: List[task_schemas.ProjectInfo] = []

    if len(result_project_list) == 0:
        return project_list
    
    for i in range(len(result_project_list)):
        query = select(Project).where(Project.c.id == result_project_list[i].get("project"))
        result = await session.execute(query)
        result_list = result.mappings().all()
        if len(result_list) > 0:
            this_project = result_list[0]
        else:
            continue

        print(this_project)

        query = select(Status).where(Status.c.project == this_project.get("id"))
        result = await session.execute(query)
        result_list = result.mappings().all()
        statuses_in_this_project: List[task_schemas.StatusInfo] = []
        for i in range(len(result_list)):
            statuses_in_this_project.append(
                task_schemas.StatusInfo(
                    project_id=this_project.get("id"),
                    status_name=result_list[i].get("status_name")
                )
            )

        query = select(User_Project).where(User_Project.c.project == this_project.get("id"))
        result = await session.execute(query)
        result_list = result.mappings().all()
        print(result_list)
        mentors_list: List[UserInfo] = []
        student_list: List[UserInfo] = []

        for i in range(len(result_list)):
            user = await db_utils.get_current_user_by_index(session, result_list[i].get("user"))
            print(user)
            if user.get("profile_type") == ProfileType.mentor:
                mentors_list.append(
                    UserInfo(
                        index=user.get("id"),
                        name=user.get("name"),
                        surname=user.get("surname"),
                        email=user.get("email"),
                        profile_type=user.get("profile_type"),
                        is_active=user.get("is_active")
                    )
                )
            elif user.get("profile_type") == ProfileType.student:
                student_list.append(
                    UserInfo(
                        index=user.get("id"),
                        name=user.get("name"),
                        surname=user.get("surname"),
                        email=user.get("email"),
                        profile_type=user.get("profile_type"),
                        is_active=user.get("is_active")
                    )
                )
        
        project_list.append(
            task_schemas.ProjectInfo(
                index=this_project.get("id"),
                title=this_project.get("title"),
                description=this_project.get("description"),
                create_at=this_project.get("create_at"),
                columens=statuses_in_this_project,
                mentors=mentors_list,
                students=student_list
            )
        )

    return project_list

@router.get("/{project_id}")
async def get_information_about_project(
    project_id: int,
    payload: dict = Depends(tsk_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> task_schemas.ProjectInfo:
    
    query = select(Project).where(Project.c.id == project_id)
    result = await session.execute(query)
    result_list = result.mappings().all()
    if len(result_list) == 0: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    else: 
        this_project = result_list[0]

    query = select(User_Project).where(
        User_Project.c.user == payload.get("sub"), 
        User_Project.c.project == project_id)
    result = await session.execute(query)
    result_list = result.mappings().all()
    print(result_list)
    if len(result_list) == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of this project"
        )

    query = select(Status).where(Status.c.project == this_project.get("id"))
    result = await session.execute(query)
    result_list = result.mappings().all()
    statuses_in_this_project: List[task_schemas.StatusInfo] = []
    for i in range(len(result_list)):
        statuses_in_this_project.append(
            task_schemas.StatusInfo(
                project_id=this_project.get("id"),
                status_name=result_list[i].get("status_name")
            )
        )

    query = select(User_Project).where(User_Project.c.project == this_project.get("id"))
    result = await session.execute(query)
    result_list = result.mappings().all()
    print(result_list)
    mentors_list: List[UserInfo] = []
    student_list: List[UserInfo] = []

    for i in range(len(result_list)):
        user = await db_utils.get_current_user_by_index(session, result_list[i].get("user"))
        print(user)
        if user.get("profile_type") == ProfileType.mentor:
            mentors_list.append(
                UserInfo(
                    index=user.get("id"),
                    name=user.get("name"),
                    surname=user.get("surname"),
                    email=user.get("email"),
                    profile_type=user.get("profile_type"),
                    is_active=user.get("is_active")
                )
            )
        elif user.get("profile_type") == ProfileType.student:
            student_list.append(
                UserInfo(
                    index=user.get("id"),
                    name=user.get("name"),
                    surname=user.get("surname"),
                    email=user.get("email"),
                    profile_type=user.get("profile_type"),
                    is_active=user.get("is_active")
                )
            )
    
    return task_schemas.ProjectInfo(
        index=this_project.get("id"),
        title=this_project.get("title"),
        description=this_project.get("description"),
        create_at=this_project.get("create_at"),
        columens=statuses_in_this_project,
        mentors=mentors_list,
        students=student_list
    )

@router.post("/add")
async def add_project(
    project_info: task_schemas.AddProject,
    payload: dict = Depends(tsk_utils.get_current_token_payload),
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

        for i in range(3):
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
            user_in_project: dict = {
                "user": project_info.mentors[i].index,
                "project": this_project.get("id")
            }
            stmt = insert(User_Project).values(user_in_project)
            await session.execute(stmt)
    await session.commit()

    if len(project_info.students) >= 1:
        if project_info.students[0].index != 0:
            for i in range(len(project_info.students)):
                user_in_project: dict = {
                "user": project_info.students[i].index,
                "project": this_project.get("id")
                }
                stmt = insert(User_Project).values(user_in_project)
                await session.execute(stmt)
        await session.commit()

    query = select(Status).where(Status.c.project == this_project.get("id"))
    result = await session.execute(query)
    result_list = result.mappings().all()
    statuses_in_this_project: List[task_schemas.StatusInfo] = []
    for i in range(len(result_list)):
        statuses_in_this_project.append(
            task_schemas.StatusInfo(
                project_id=this_project.get("id"),
                status_name=result_list[i].get("status_name")
            )
        )

    query = select(User_Project).where(User_Project.c.project == this_project.get("id"))
    result = await session.execute(query)
    result_list = result.mappings().all()
    print(result_list)
    mentors_list: List[UserInfo] = []
    student_list: List[UserInfo] = []

    for i in range(len(result_list)):
        user = await db_utils.get_current_user_by_index(session, result_list[i].get("user"))
        print(user)
        if user.get("profile_type") == ProfileType.mentor:
            mentors_list.append(
                UserInfo(
                    index=user.get("id"),
                    name=user.get("name"),
                    surname=user.get("surname"),
                    email=user.get("email"),
                    profile_type=user.get("profile_type"),
                    is_active=user.get("is_active")
                )
            )
        elif user.get("profile_type") == ProfileType.student:
            student_list.append(
                UserInfo(
                    index=user.get("id"),
                    name=user.get("name"),
                    surname=user.get("surname"),
                    email=user.get("email"),
                    profile_type=user.get("profile_type"),
                    is_active=user.get("is_active")
                )
            )
                    

    return task_schemas.ProjectInfo(
        index=this_project.get("id"),
        title=this_project.get("title"),
        description=this_project.get("description"),
        create_at=this_project.get("create_at"),
        columens=statuses_in_this_project,
        mentors=mentors_list,
        students=student_list
    )

@router.put("/{project_id}")
async def change_information_about_project(
    project_id: int,
    new_project_info: task_schemas.AddProject,
    payload: dict = Depends(tsk_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)) -> task_schemas.ProjectInfo:
    pass

@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    payload: dict = Depends(tsk_utils.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)):

    if payload.get("profile_type") != ProfileType.mentor.name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )
    
    stmt = delete(Project).where(Project.c.id == project_id)
    await session.execute(stmt)
    await session.commit()

    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Project deleted"
    )
