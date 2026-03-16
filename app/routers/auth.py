from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. database import get_db
from .. import  db_models, schemas, utils, oauth2


router = APIRouter(
    tags= ['Authentication']
)

@router.post('/login', response_model= schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db : Session =  Depends(get_db)):
    # OAuth2PasswordRequestForm  -> it converts any input thing during login as a username & password irrespective of it may be id, email or etc.

    user = db.query(db_models.User).filter(db_models.User.email == user_credential.username).first()

    if not user:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    
    if not utils.verify_user(user_credential.password, user.password):
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    
    # create Token
    # return the token 
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type":"bearer"}
    


    
