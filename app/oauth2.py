import re
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


#SECRET_KEY
#Algorithm
#Expiration time 


SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


    return encoded_jwt


def verify_acess_token(token: str, credentials_exeception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:str = payload.get('user_id')

        if id is None:
            raise credentials_exeception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exeception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exeception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail="could no validate credentials", headers={"WWW-Authenticate": "Bearer"})

    user = verify_acess_token(token, credentials_exeception)

    return user
