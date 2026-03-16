from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:2003%40@localhost/Fastapi'   # %40 <==> @

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