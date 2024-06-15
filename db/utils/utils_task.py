from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from db.models.task_model import task as TaskModel
from api.auth.schemas.schemas import UserInfo
from api.tasks.schemas.schemas import TaskInfo, AddTask

async def add_task_in_db(
    task: dict,
    session: AsyncSession
) -> bool:
    try:
        stmt = insert(TaskModel).values(task)
        await session.execute(stmt)
        await session.commit()
    except:
        return False
    return True

async def get_all_tasks_for_student(
    student: UserInfo,
    session: AsyncSession
) -> List[TaskInfo]:
    
    stmt = select(TaskModel).where(TaskModel.c.student == student.index)
    task_list_in_db = await session.execute(stmt)
    task_list = task_list_in_db.mappings().all()

    result_list: List[TaskInfo] = []

    for task in task_list:
        result_list.append(
            TaskInfo(
                index=task.get("id"),
                title=task.get("title"),
                description=task.get("description"),
                create_at=task.get("create_at"),
                start_task=task.get("start_task"),
                finish_task=task.get("finish_task"),
                score=task.get("score"),
                status=task.get("status"),
                student=task.get("student"),
                mentor=task.get("mentor")
            )
        )
    
    return result_list

async def get_all_tasks_for_mentor(
    mentor: UserInfo,
    session: AsyncSession
) -> List[TaskInfo]:
    
    stmt = select(TaskModel).where(TaskModel.c.mentor == mentor.index)
    task_list_in_db = await session.execute(stmt)
    task_list = task_list_in_db.mappings().all()

    result_list: List[TaskInfo] = []

    for task in task_list:
        result_list.append(
            TaskInfo(
                index=task.get("id"),
                title=task.get("title"),
                description=task.get("description"),
                create_at=task.get("create_at"),
                start_task=task.get("start_task"),
                finish_task=task.get("finish_task"),
                score=task.get("score"),
                status=task.get("status"),
                student=task.get("student"),
                mentor=task.get("mentor")
            )
        )
    
    return result_list

async def get_task_by_index(
    index: int,
    session: AsyncSession,
) -> TaskInfo:
    stmt = select(TaskModel).where(TaskModel.c.id == index)

    task_in_db = await session.execute(stmt)
    task_list = task_in_db.mappings().all()

    if len(task_list) > 0:
        task: dict = task_list[0]
    else: 
        return None
    
    return TaskInfo(
        index=task.get("id"),
        title=task.get("title"),
        description=task.get("description"),
        create_at=task.get("create_at"),
        start_task=task.get("start_task"),
        finish_task=task.get("finish_task"),
        score=task.get("score"),
        status=task.get("status"),
        student=task.get("student"),
        mentor=task.get("mentor")
    )

async def delete_task_by_index(
    index: int,
    session: AsyncSession,
):
    try:
        stmt = delete(TaskModel).where(TaskModel.c.id == index)
        await session.execute(stmt)
        await session.commit()
    except:
        return False
    return True

async def change_task_info(
    index: int,
    new_task_info: AddTask,
    session: AsyncSession
) -> TaskInfo:
    stmt = select(TaskModel).where(TaskModel.c.id == index)
    task_in_db = await session.execute(stmt)
    task_list = task_in_db.mappings().all()

    if len(task_list) > 0:
        task: dict = task_list[0]
    else: 
        return None
    
    if task.get("title") != new_task_info.title:
        stmt = update(TaskModel).where(TaskModel.c.id == index).values(title=new_task_info.title)
        await session.execute(stmt)
        
    if task.get("description") != new_task_info.description:
        stmt = update(TaskModel).where(TaskModel.c.id == index).values(description=new_task_info.description)
        await session.execute(stmt)

    if task.get("start_task") != new_task_info.start_task:
        stmt = update(TaskModel).where(TaskModel.c.id == index).values(start_task=new_task_info.start_task) 
        await session.execute(stmt)

    if task.get("finish_task") != new_task_info.finish_task:
        stmt = update(TaskModel).where(TaskModel.c.id == index).values(finish_task=new_task_info.finish_task)
        await session.execute(stmt)

    if task.get("status") != new_task_info.status:
        stmt = update(TaskModel).where(TaskModel.c.id == index).values(status=new_task_info.status)
        await session.execute(stmt)

    if task.get("score") != new_task_info.score:
        if new_task_info.score > 100: new_task_info.score = 100
        stmt = update(TaskModel).where(TaskModel.c.id == index).values(score=new_task_info.score)
        await session.execute(stmt)

    await session.commit()

    return await get_task_by_index(index, session)


async def get_all_tasks(
    session: AsyncSession
) -> List[TaskInfo]:
    
    stmt = select(TaskModel).where(TaskModel.c.id > 0)
    tasks_db = await session.execute(stmt)
    task_list = tasks_db.mappings().all()

    result_list: List[TaskInfo] = []

    for task in task_list:
        result_list.append(
            TaskInfo(
                index=task.get("id"),
                title=task.get("title"),
                description=task.get("description"),
                create_at=task.get("create_at"),
                start_task=task.get("start_task"),
                finish_task=task.get("finish_task"),
                score=task.get("score"),
                status=task.get("status"),
                student=task.get("student"),
                mentor=task.get("mentor")
            )
        )

    return result_list