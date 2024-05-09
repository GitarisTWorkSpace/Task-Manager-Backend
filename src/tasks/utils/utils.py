from tasks.models.models import project as Project, status as Status, user_in_project as User_Project
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import tasks.schemas.schemas as task_schemas
import auth.utils.utils_db as db_utils
from auth.schemas.schemas import UserInfo
from auth.models.models import ProfileType

async def get_project_information_by_index(
    session: AsyncSession,
    project_id: int
    ) -> list: 
    query = select(Project).where(Project.c.id == project_id)
    result = await session.execute(query)
    result_list = result.mappings().all()
    if len(result_list) > 0:
        return result_list[0]
    else:
        return None
    
async def get_columens_in_project(
    session: AsyncSession,
    project_id: int
    ) -> List[task_schemas.StatusInfo]:
    query = select(Status).where(Status.c.project == project_id)
    result = await session.execute(query)
    result_list = result.mappings().all()

    statuses_in_this_project: List[task_schemas.StatusInfo] = []

    for i in range(len(result_list)):
        statuses_in_this_project.append(
            task_schemas.StatusInfo(
                project_id=project_id,
                status_name=result_list[i].get("status_name")
            )
        )

    return statuses_in_this_project

async def get_users_in_project(
    session: AsyncSession,
    project_id: int
    ) -> list:
    query = select(User_Project).where(User_Project.c.project == project_id)
    result = await session.execute(query)
    result_list = result.mappings().all()
    if len(result_list) > 0:
        return result_list
    else:
        return None

async def metors_list_in_project(
    session: AsyncSession,
    project_id: int
    ) -> List[UserInfo]:
    user_list = await get_users_in_project(session, project_id)

    mentors_list: List[UserInfo] = []

    if user_list == None:
        return mentors_list

    for i in range(len(user_list)):
        user = await db_utils.get_current_user_by_index(session, user_list[i].get("user"))

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
            continue
    
    return mentors_list

async def students_list_in_project(
    session: AsyncSession,
    project_id: int
    ) -> List[UserInfo]:
    user_list = await get_users_in_project(session, project_id)

    student_list: List[UserInfo] = []

    if user_list == None:
        return student_list

    for i in range(len(user_list)):
        user = await db_utils.get_current_user_by_index(session, user_list[i].get("user"))
        if user.get("profile_type") == ProfileType.student:
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
        elif user.get("profile_type") == ProfileType.mentor:
            continue
    
    return student_list

async def get_information_about_project_by_index(
    session: AsyncSession,
    project_id: int
    ) -> task_schemas.ProjectInfo:
    
    this_project = await get_project_information_by_index(session, project_id)

    # Get columens in project 
    columens_in_this_project = await get_columens_in_project(session, project_id)

    # Get users in project
    user_list = await get_users_in_project(session, project_id)

    # Mentors and student lists
    mentors_list: List[UserInfo] = await metors_list_in_project(session, project_id)
    student_list: List[UserInfo] = await students_list_in_project(session, project_id)

    this_project = task_schemas.ProjectInfo(
        index=this_project.get("id"),
        title=this_project.get("title"),
        description=this_project.get("description"),
        create_at=this_project.get("create_at"),
        columens=columens_in_this_project,
        mentors=mentors_list,
        students=student_list
    )

    return this_project
