from fastapi import  HTTPException, status, Depends, APIRouter
from .. import db_models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= '/users',
    tags= ['Users']
)

@router.post('/', status_code= status.HTTP_201_CREATED, response_model= schemas.UserCreateResponse)
def create_user(user_data: schemas.UserCreate, db:Session = Depends(get_db)):
     # convert password into hash password
     hashed_password =  utils.hash(user_data.password)
     user_data.password = hashed_password
     new_user  = db_models.User(**user_data.dict())  # passing all the user input to the db schema 
     db.add(new_user)
     db.commit()
     db.refresh(new_user)  # this helps to retrieve the currently pushed data from the db and stored in the new_post variable
     return new_user


@router.get('/{id}', response_model= schemas.UserCreateResponse)
def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(db_models.User).filter(db_models.User.id == id)
    if user.first() is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.first()