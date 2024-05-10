from tasks.models.models import project as Project, status as Status, user_in_project as User_Project, task as Task
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
    
async def  check_user_in_project(
    session: AsyncSession,
    user_id: int,
    project_id: int
) -> bool:
    query = select(User_Project).where(
        User_Project.c.user == user_id, 
        User_Project.c.project == project_id)
    result = await session.execute(query)
    print(result)
    result_list = result.mappings().all()
    print(len(result_list))
    
    if len(result_list) >= 1:
        return True
    else:
        return False
    

async def get_columen_by_index_in_project(
    session: AsyncSession,
    project_id: int,
    columen_id: int
    ) -> task_schemas.StatusInfo:
    query = select(Status).where(
        Status.c.id == columen_id, 
        Status.c.project == project_id)

    result = await session.execute(query)
    result_list = result.mappings().all()

    if len(result_list) > 0:
        columen_info = result_list[0]
    else: 
        return None
    
    return task_schemas.StatusInfo(
        index=columen_id,
        project_id=project_id,
        status_name=columen_info.get("status_name")
    )

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
                index=result_list[i].get("id"),
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

    project = task_schemas.ProjectInfo(
        index=this_project.get("id"),
        title=this_project.get("title"),
        description=this_project.get("description"),
        create_at=this_project.get("create_at"),
        columens=columens_in_this_project,
        mentors=mentors_list,
        students=student_list
    )

    return project


async def get_information_about_task(
    session: AsyncSession,
    project_id: int,
    task_id: int
    ) -> task_schemas.TaskInfo:

    query = select(Task).where(Task.c.project == project_id, Task.c.id == task_id)
    result = await session.execute(query)
    result_list = result.mappings().all()

    if len(result_list) > 0:
        task_info: dict = result_list[0]
    else: 
        return None
    
    mentor: UserInfo = await db_utils.get_user_by_id(session, task_info.get("mentor"))
    student: UserInfo = await db_utils.get_user_by_id(session, task_info.get("student"))
    status: task_schemas.StatusInfo = await get_columen_by_index_in_project(session, project_id, task_info.get("status"))

    task: task_schemas.TaskInfo = task_schemas.TaskInfo(
        index=task_info.get("id"),
        project=task_info.get("project"),
        title=task_info.get("title"),
        description=task_info.get("description"),
        create_at=task_info.get("create_at"),
        date_start=task_info.get("date_start"),
        date_finish=task_info.get("date_finish"),
        assessment=task_info.get("assessment"),
        status=status,
        mentor=mentor,
        student=student
    )

    return task
