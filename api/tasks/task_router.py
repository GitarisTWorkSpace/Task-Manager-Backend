from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from db.sesion import get_async_session
from db.utils import utils_user, utils_task
from api.auth.schemas.schemas import Role
from api.auth.schemas.schemas import UserInfo
from api.tasks.schemas.schemas import AddTask, TaskInfo
from api.auth.utils import utils_jwt

task_router = APIRouter(prefix="/task", tags=["Task"])

@task_router.get("/all", response_model=List[TaskInfo])
async def get_all_access_tasks(
    payload: dict = Depends(utils_jwt.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    user_in_db: dict = await utils_user.get_current_user_by_index(session, payload.get("sub"))
    user: UserInfo = utils_user.user_in_db_transform_in_user_info(user_in_db)

    return await utils_task.get_all_tasks_for_student(student=user, session=session)

@task_router.get("/{index}", response_model=TaskInfo)
async def get_task_info(
    index: int,
    payload: dict = Depends(utils_jwt.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    user_in_db: dict = await utils_user.get_current_user_by_index(session, payload.get("sub"))
    user: UserInfo = utils_user.user_in_db_transform_in_user_info(user_in_db)

    task_in_db = await utils_task.get_task_by_index(index, session)

    if task_in_db.student != user.index:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not you task"
        )
    
    return task_in_db

@task_router.post("/add")
async def add_task(
    new_task: AddTask,
    payload: dict = Depends(utils_jwt.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    user_in_db: dict = await utils_user.get_current_user_by_index(session, payload.get("sub"))
    user: UserInfo = utils_user.user_in_db_transform_in_user_info(user_in_db)

    task: dict = {
        "title": new_task.title,
        "description": new_task.description,
        "create_at": datetime.utcnow(),
        "start_task": new_task.start_task,
        "finish_task": new_task.finish_task,
        "status": new_task.status
    }

    if user.role == Role.student.name:
        task.update(
            student=user.index,
            mentor=new_task.mentor # Пока не сделаю таблицу с привязкой наставников и стажоров
        )

    task.update(
        score=new_task.score,
        student=new_task.student, # как сделаю связи надо будет тоже проверку проводить
        mentor=new_task.mentor # как сделаю связи надо будет тоже проверку проводить
    )

    if not await utils_task.add_task_in_db(task, session):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Task not created"
        )
    
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Task created"
    )

@task_router.put("/{index}", response_model=TaskInfo)
async def change_task(
    index: int,
    new_task_info: AddTask,
    payload: dict = Depends(utils_jwt.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    user_in_db: dict = await utils_user.get_current_user_by_index(session, payload.get("sub"))
    user: UserInfo = utils_user.user_in_db_transform_in_user_info(user_in_db)

    task_in_db = await utils_task.get_task_by_index(index, session)

    if task_in_db.student != user.index:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not you task"
        )
    
    return await utils_task.change_task_info(index, new_task_info, session)

@task_router.delete("/{index}}")
async def delete_task(
    index: int,
    payload: dict = Depends(utils_jwt.get_current_token_payload),
    session: AsyncSession = Depends(get_async_session)
):
    user_in_db: dict = await utils_user.get_current_user_by_index(session, payload.get("sub"))
    user: UserInfo = utils_user.user_in_db_transform_in_user_info(user_in_db)

    task_in_db = await utils_task.get_task_by_index(index, session)

    if task_in_db.student != user.index:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not you task"
        )
    
    if not await utils_task.delete_task_by_index(index, session):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Couldn't delete task"
        )

    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Task deleted"
    )