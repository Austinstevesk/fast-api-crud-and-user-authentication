from fastapi import FastAPI, status, HTTPException, Response, APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, models, utils #You can move up 2 steps using ..
from ..database import get_db


router = APIRouter()

@router.post('/users/new', status_code=status.HTTP_201_CREATED, response_model=schemas.CreateUserResponse)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/users/{id}', response_model=schemas.CreateUserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id: {id} does not exist'))

    return user