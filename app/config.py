from dotenv  import load_dotenv
import os
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
HOST= os.getenv("HOST")
DATABASE= os.getenv("DATABASE")
USER=os.getenv("USER") 
PASSWORD=os.getenv("PASSWORD")
