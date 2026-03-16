from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine
from . import db_models
from . routers import post, user, auth
from .config import USER, DATABASE, PASSWORD, HOST


# SQL Alachemy
db_models.Base.metadata.create_all(bind = engine)

app = FastAPI()


    
while True:  # This loop helps to connect the fastapi server to postgre database until it is connected, then it moves to backend endpoints, used only in case of if only db driver is used.
        
        try:
            conn =  psycopg2.connect(host = HOST, database = DATABASE, user = USER, 
                             password = PASSWORD, cursor_factory= RealDictCursor)  
            # cursor_factory= RealDictCursor ==> It maps the columns with the values

            cursor  = conn.cursor()
            print("Database Connected Sucessfully")
            break 

        except Exception as error:
         print("Connecting to Database Failed")
         print("Error: ", error)

         time.sleep(2) # For every 2 second server try to connect with database 



@app.get('/')
def root():
    return {"message":"Hello world"}

# Verify the user
app.include_router(auth.router)

# All the routes of posts is called by this
app.include_router(post.router)

# All the routes of user is called by this
app.include_router(user.router)






# run : fastapi dev main.py
# or 
# uvicorn main:app --reload