from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)

@router.get("/", response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    #Initially this is the way to fetch
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

#title str, content str
@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.UpdatePost, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #Initial query
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user)
    new_post = models.Post(**post.dict()) 
    #The above unpacks all the data at a go instead of getting all the fields manually
    print(new_post)
    #models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": {"title": payload['title'], "content":payload['content']}}




# #This route cannot be below the /posts/{id} route since it could match the unrelated route
# @router.get("/latest")
# def get_latest_post(db: Session = Depends(get_db)):
#     latest_post = db.query(models.User).filter(models.Post.created_at)

    return latest_post

@router.get("/{id}", response_model=schemas.PostResponse)
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
    return post


# def find_post_index(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.put("/update/{id}")
def update_post(id: int, post: schemas.UpdatePost, db: Session = Depends(get_db)):
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
    return post_query.first()
