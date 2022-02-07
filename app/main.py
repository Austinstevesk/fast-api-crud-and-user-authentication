from builtins import int, print, str
from multiprocessing import synchronize
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

#bind the models
models.Base.metadata.create_all(bind=engine)


#create the app instance
app = FastAPI()


my_posts = [{"title":"First post", "content":"First post content", "id":1}, {"title":"favourite foods", "content": "I like pizza", "id":2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
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


#Route to test sqlalchemy
@app.route('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    return {'status': 'sucess'}


@app.get("/")
async def root():
    return {"Message": "Welcome"}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    #Initially this is the way to fetch
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    print(posts)
    return {"data": posts}

#title str, content str
@app.post("/posts/create", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session=Depends(get_db)):
    #Initial query
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict()) 
    #The above unpacks all the data at a go instead of getting all the fields manually
    print(new_post)
    #models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": {"title": payload['title'], "content":payload['content']}}




#This route cannot be below the /posts/{id} route since it could match the unrelated route
@app.get("/posts/latest")
def get_latest_post():
    latest = my_posts[-1]
    print(my_posts)
    return {"latest_post": latest}
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    #post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message": f'post with id: {id} was not found'}
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found'))
    return{"post_detail": post}


# def find_post_index(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

@app.delete("/posts/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    #delete a post
    #find the index of the post
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id {id} does not exist"))

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    #my_posts.pop(index)


@app.put("/posts/update/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id )))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    #updated_post only allows us to store a value but it does not represent the schema
    updated_post = post_query.first()

    if updated_post == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"A post with id {id} does not exist"))


    #the post.dict() is the data parsed in by the user, don't confuse with the updated_post
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}


@app.patch("/posts/update/patch/{id}")
def update_post(id: int, post:Post):
    index = find_post_index(id)
    if index == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"A post with id {id} does not exist"))
    post_dict = post.dict()
    my_posts[index] = post_dict
    post_dict['id'] = id
    print(post)
    print(post_dict)
    return {"data": post_dict}