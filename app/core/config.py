from pydantic_settings import BaseSettings


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
    
    class Config:
        env_file = ".env"


settings = Settings()