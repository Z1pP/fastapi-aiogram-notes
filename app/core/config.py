from pathlib import Path
from typing import Literal
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent.parent


class RateLimited(BaseModel):
    total_request: int = 10
    period: Literal["hour", "minute"] = "hour"
    redis_url: str = "redis://localhost:6379"


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7  # 1 week
    token_type: str = "Bearer"


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    BOT_TOKEN: str
    authjwt: AuthJWT = AuthJWT()
    rate_limit: RateLimited = RateLimited()

    class Config:
        env_file = ".env"


settings = Settings()
