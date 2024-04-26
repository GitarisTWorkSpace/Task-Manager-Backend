from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from db.models.models import UserSchema
import auth.schemas as schemas
import auth.utils_jwt as auth_utils

http_bearer = HTTPBearer()

router = APIRouter(prefix="/jwt", tags=["Auth"])

john = UserSchema(   
    username="john",
    password=auth_utils.hash_password("qwerty"),
    email="john@exmple.com"
)

sam = UserSchema(
    username="sam",
    password=auth_utils.hash_password("secret"),
)

user_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam 
}

@router.post("/registration/", response_model=schemas.UserInfo)
def registration_user(user: schemas.UserRegistration):
    pass

def validate_auth_user(
    username: str,
    password: str
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password"
    )
    if not (user := user_db.get(username)):
        raise unauthed_exc
    
    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password
    ):
        raise unauthed_exc
    
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive"
        )
    
    return user
    
    

@router.post("/login/", response_model=schemas.TokenInfo)
def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user)):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email
    }
    accesss_token = auth_utils.encode_jwt(jwt_payload, )
    return schemas.TokenInfo(
        access_token=accesss_token,
        token_type="Bearer"
    )

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

def get_current_auth_user(payload: dict = Depends(get_current_token_payload)) -> UserSchema:
    username: str = payload.get("sub")
    if user := user_db.get(username):
        return user
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid"
    )

def get_current_active_auth_user(user: UserSchema = Depends(get_current_auth_user)):
    if user.active:
        return user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive"
    )

@router.get("/me")
def auth_user_check_self_info(user: UserSchema = Depends(get_current_active_auth_user)):
    return {
        "username": user.username,
        "email": user.email
    }