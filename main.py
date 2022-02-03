from typing import Optional
from fastapi import FastAPI
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
@app.post("/posts/create")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data": post_dict}
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": {"title": payload['title'], "content":payload['content']}}


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        else:
            return "No such post"

@app.get("/posts/{id}")
def get_post(id: int):
    print(id)
    post = find_post(id)
    print(post)
    return{"post_detail": post}