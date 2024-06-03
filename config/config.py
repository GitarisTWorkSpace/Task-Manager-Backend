import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path
from enum import Enum

BASE_DIR = Path(__file__).parent.parent

load_dotenv()

class Role(Enum):
    admin = "Администратор"
    hr = "HR"
    manage = "Менаджер"
    mentor = "Наставник"
    student = "Стажер"

class TokenInfo(BaseModel):
    TOKEN_TYPE_FIELD: str = "type"
    ACCESS_TOKEN_TYPE: str = "access"
    REFRESH_TOKEN_TYPE: str = "refresh"


class DbSettings(BaseModel):
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT")
    DATABASE_URL: str = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    DATABASE_URL_ASYNC: str = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "api" / "auth" / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "api" / "auth" / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30

class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    db_settings: DbSettings = DbSettings()
    token_info: TokenInfo = TokenInfo()

settings = Settings()