from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings
from urllib.parse import quote_plus

password = quote_plus(settings.PASSWORD)
SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{settings.USER}:{password}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE}' # %40 <==> @

engine =  create_engine(SQLALCHEMY_DATABASE_URL)

Session_Local = sessionmaker(autocommit = False, autoflush=False, bind = engine)

Base = declarative_base()  # All the tables or we can say models, they inheriting from this base class


# dependency  -> sent a db request when endpoint hit request executed then the db seesion is closed
def get_db():
    db = Session_Local()
    try:
        yield db
    finally:
        db.close()


# This only we used when you need to apply raw sql coomands and conncet to database, but sqlalchemy do on top of psycopg2.

# from .config import settings
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# while True:  # This loop helps to connect the fastapi server to postgre database until it is connected, then it moves to backend endpoints, used only in case of if only db driver is used.
        
#         try:
#             conn =  psycopg2.connect(host = settings.HOST, database = settings.DATABASE, user = settings.USER, 
#                              password = settings.PASSWORD, cursor_factory= RealDictCursor)  
#             # cursor_factory= RealDictCursor ==> It maps the columns with the values

#             cursor  = conn.cursor()
#             print("Database Connected Sucessfully")
#             break 

#         except Exception as error:
#          print("Connecting to Database Failed")
#          print("Error: ", error)

#          time.sleep(2) # For every 2 second server try to connect with database 
