from builtins import int, print, str
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

my_posts = [{"title":"First post", "content":"First post content", "id":1}, {"title":"favourite foods", "content": "I like pizza", "id":2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]=None 

@app.get("/")
async def root():
    return {"Message": "Welcome"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

#title str, content str
@app.post("/posts/create", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data": post_dict}
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
def get_post(id: int, response: Response):
    print(id)   
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message": f'post with id: {id} was not found'}
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found'))
    print(post)
    return{"post_detail": post}


def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.delete("/posts/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #delete a post
    #find the index of the post
    index = find_post_index(id)
    print(index)
    if index == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id {id} does not exist"))
    my_posts.pop(index)
    print(my_posts)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    #my_posts.pop(index)


@app.put("/posts/update/{id}")
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