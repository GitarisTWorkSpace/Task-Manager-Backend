from fastapi import APIRouter, Depends, HTTPException, status
from db.sesion import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from db.utils import utils_user, utils_connection
from api.auth.utils import utils_jwt
from api.auth.schemas.schemas import Role
from api.auth.schemas.schemas import UserInfo
from api.connection.schemas.schemas import AddConnection, Connection, ChangeConection

connection_router = APIRouter(prefix='/connection', tags=["Connection"])

@connection_router.post("/add")
async def connection_mentor_and_student(
    new_connection: AddConnection,
    payload: dict = Depends(utils_jwt.validate_token_type_is_access),
    session: AsyncSession = Depends(get_async_session)
):
    
    user_in_db: dict = await utils_user.get_current_user_by_index(session, payload.get("sub"))
    user: UserInfo = utils_user.user_in_db_transform_in_user_info(user_in_db)

    if not (user.role == Role.admin or user.role == Role.manager):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    mentor_in_db = await utils_user.get_current_user_by_index(session, new_connection.mentor)
    mentor: UserInfo = utils_user.user_in_db_transform_in_user_info(mentor_in_db)

    if mentor.role != Role.mentor:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Mentor is not role 'mentor'"
        )
    
    for student in new_connection.students:
        student_in_db = await utils_user.get_current_user_by_index(session, student.index)
        student_user: UserInfo = utils_user.user_in_db_transform_in_user_info(student_in_db)
        if student_user.role != Role.student:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"User {student.name!r} not role is 'student'"
            )
    
    if not await utils_connection.add_connections_in_db(new_connection, session):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Connection not created"
        )
    
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Connection created"
    )

@connection_router.get("/mentor/{index}", response_model=Connection)
async def get_student_connection_with_mentor(
    index: int,
    payload: dict = Depends(utils_jwt.validate_token_type_is_access),
    session: AsyncSession = Depends(get_async_session)
): 
    
    user_in_db: dict = await utils_user.get_current_user_by_index(session, payload.get("sub"))
    user: UserInfo = utils_user.user_in_db_transform_in_user_info(user_in_db)

    if not (user.role == Role.admin or user.role == Role.manager):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return await utils_connection.get_conection_by_mentor_index(index, session)

@connection_router.put("/mentor/{index}")
async def delete_student_for_mentor(
    index: int,
    student_list: ChangeConection,
    payload: dict = Depends(utils_jwt.validate_token_type_is_access),
    session: AsyncSession = Depends(get_async_session)
):
    user_in_db: dict = await utils_user.get_current_user_by_index(session, payload.get("sub"))
    user: UserInfo = utils_user.user_in_db_transform_in_user_info(user_in_db)

    if not (user.role == Role.admin or user.role == Role.manager):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    

@connection_router.get('/connected')
def connection_students():
    pass


@connection_router.get('/none')
def not_connection_students():
    pass