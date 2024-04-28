import jwt 
import bcrypt
from datetime import timedelta, datetime
from config.config import settings

def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_timedelta: timedelta | None = None,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes
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
    encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm);
    return encoded

def decoded_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt();
    pwd_bytes: bytes = password.encode() 
    return bcrypt.hashpw(pwd_bytes, salt=salt)

def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)