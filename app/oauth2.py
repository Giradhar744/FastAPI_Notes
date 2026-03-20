from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from .import schemas, database, db_models
from sqlalchemy.orm import Session
from . config import settings

# Secret key
# Algorithm
# Expiration Time after the user logged in


oauth2_scheme =  OAuth2PasswordBearer(tokenUrl='login')  # OAuth2PasswordBearer extracts token

def create_access_token (data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm= settings.ALGORITHM)

    return encoded_jwt


def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms= [settings.ALGORITHM])
        login_id :str = payload.get("user_id")

        if not login_id:
            raise credentials_exception
        
        token_data = schemas.Token_data(id = login_id)
        return token_data
    
    except JWTError:
        raise credentials_exception
    
   
   
def get_current_user(token : str =  Depends(oauth2_scheme), db : Session = Depends(database.get_db)):   # get_current_user() receives token via Depends()
 # Depends() tells FastAPI to run another function first and inject its result into the current function.

    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Could not validate the credentials",
                                          headers= {"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token , credentials_exception) 

    user = db.query(db_models.User).filter(db_models.User.id == token.id).first()

    return  user   # return db_model object
