from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

from .routers import posts, users, auth


#bind the models
models.Base.metadata.create_all(bind=engine)

#create the app instance
app = FastAPI()


# my_posts = [{"title":"First post", "content":"First post content", "id":1}, {"title":"favourite foods", "content": "I like pizza", "id":2}]

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', dbname='fastapi', user='', password='', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection is successful")
#         break

#     except Exception as error:
#         print("Connection failed")
#         print("Error: ", error)
        # time.sleep(2)



app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

#Route to test sqlalchemy
@app.route('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    return {'status': 'success'}


@app.get("/")
async def root():
    return {"Message": "Welcome"}

