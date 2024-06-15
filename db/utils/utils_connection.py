from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from api.auth.schemas.schemas import UserInfo
from db.utils import utils_user
from db.models.connection_model import connection as ConnectModel
from api.connection.schemas.schemas import AddConnection, Connection, ChangeConection

async def add_connections_in_db(
    connections: AddConnection,
    session: AsyncSession
):
    for student in connections.students:
        new_conection: dict = {
            "student": student.index,
            "mentor": connections.mentor
        }
        stmt = insert(ConnectModel).values(new_conection)
        await session.execute(stmt)

    try: 
        await session.commit()
        return True
    except:
        return False
    
async def get_conection_by_mentor_index(
    mentor_index: int,
    session: AsyncSession
):
    stmt = select(ConnectModel).where(ConnectModel.c.mentor == mentor_index)
    connection_id_db = await session.execute(stmt)
    connections = connection_id_db.mappings().all() 

    #print(connections)

    mentor_in_db = await utils_user.get_current_user_by_index(session, mentor_index)
    mentor: UserInfo = utils_user.user_in_db_transform_in_user_info(mentor_in_db)
    
    student_list: List[UserInfo] = []

    for user in connections:
        #print(user)
        student_index = user.get("student")
        student_in_db = await utils_user.get_current_user_by_index(session, student_index)
        student: UserInfo = utils_user.user_in_db_transform_in_user_info(student_in_db)
        student_list.append(student)

    return Connection(
        mentor=mentor,
        students=student_list
    )

async def delete_student_for_mentor(
    students: List[UserInfo],
    session: AsyncSession
):
    for student in students:
        stmt = delete(ConnectModel).where(ConnectModel.c.student == student.index)
        await session.execute(stmt)

    try:
        await session.commit()
        return True
    except:
        return False