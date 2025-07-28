from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    DATABASE_URL: str  

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()