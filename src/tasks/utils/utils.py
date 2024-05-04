from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jwt import InvalidTokenError
import auth.utils.utils_jwt as auth_utils
import auth.utils.utils_db as db_utils
from auth.models.models import ProfileType

http_bearer = HTTPBearer()

def get_current_token_payload(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) :
    token = credentials.credentials
    try:
        payload = auth_utils.decoded_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token error"
        )
    
    return payload

async def get_information_about_project_by_index(
    session: AsyncSession,
    project_id: int) -> dict:
    pass
