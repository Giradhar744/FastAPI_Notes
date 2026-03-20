from dotenv  import load_dotenv
import os
from pydantic_settings import BaseSettings
load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_HOST: str
    DATABASE_PORT:str
    DATABASE: str
    USER: str
    PASSWORD:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int

    class Config:
        env_file = ".env"


settings = Settings()

# SECRET_KEY = os.getenv("SECRET_KEY")
# HOST= os.getenv("HOST")
# DATABASE= os.getenv("DATABASE")
# USER=os.getenv("USER") 
# PASSWORD=os.getenv("PASSWORD")
