from fastapi import FastAPI
from .database import engine
from . import db_models
from . routers import post, user, auth, votes


# SQL Alachemy
db_models.Base.metadata.create_all(bind = engine)

# Make an app object of FastAPI
app = FastAPI()


@app.get('/')
def root():
    return {"message":"Hello world"}

# Verify the user
app.include_router(auth.router)

# All the routes of posts is called by this
app.include_router(post.router)

# All the routes of user is called by this
app.include_router(user.router)


app.include_router(votes.router)

# run : fastapi dev main.py
# or 
# uvicorn main:app --reload