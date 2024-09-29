from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_hostname: str
    db_name: str
    db_username: str
    db_pass: str
    
    class Config:
        env_file = ".env"


settings = Settings()
