import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from config.config import settings

http_bearer = HTTPBearer()

def create_jwt_token(
    token_type: str, 
    token_data: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None
) -> str:
    jwt_paylaod = {settings.token_info.TOKEN_TYPE_FIELD: token_type}
    jwt_paylaod.update(token_data)
    return encode_jwt(
        jwt_paylaod,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta)    

def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algoritm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None
):
    to_encode: dict = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        iat=now,
        exp=expire
    )
    encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algoritm)
    return encoded

def decoded_jwt(
    token: str,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algoritm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(jwt=token, key=public_key, algorithms=[algoritm])
    return decoded

def get_current_token_payload(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) :
    token = credentials.credentials
    try:
        payload = decoded_jwt(token=token)        
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token error"
        )
    
    return payload

def validate_token_type_is_access(
    payload: dict = Depends(get_current_token_payload)
) -> dict:
    token_type = payload.get(settings.token_info.TOKEN_TYPE_FIELD)
    if token_type == settings.token_info.ACCESS_TOKEN_TYPE:
        return payload
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Invatid token type {token_type!r} expected {settings.token_info.ACCESS_TOKEN_TYPE!r}"
    )