from fastapi import APIRouter, status, HTTPException, Depends, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(
    tags=['Authentication'],
)

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #The data parsed should now be in form-data instead of raw>json

    #OAuth2PasswordRequestForm stores the email in a field called username.
    
    #Even though we are parsing in the email, we'll check it as a username

    #username = 
    #password = 
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user: 
        raise(HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials"))
    if not utils.verify(user_credentials.password, user.password):
        raise(HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials"))
    

    #create token
    #return token

    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}