from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    EMAIL_USER: str
    EMAIL_PASSWORD : str
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DEBUG: bool
    ENVIRONMENT: str

    class Config:
        env_file = ".env"

settings = Settings()