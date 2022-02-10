import http
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db

from .routers import posts, users


#bind the models
models.Base.metadata.create_all(bind=engine)

#create the app instance
app = FastAPI()


my_posts = [{"title":"First post", "content":"First post content", "id":1}, {"title":"favourite foods", "content": "I like pizza", "id":2}]

while True:
    try:
        conn = psycopg2.connect(host='localhost', dbname='fastapi', user='postgres', password='qweaz', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection is successful")
        break

    except Exception as error:
        print("Connection failed")
        print("Error: ", error)
        time.sleep(2)



app.include_router(posts.router)
app.include_router(users.router)

#Route to test sqlalchemy
@app.route('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    return {'status': 'success'}


@app.get("/")
async def root():
    return {"Message": "Welcome"}


