

from fastapi import FastAPI

from pydantic import BaseModel, BaseSettings


import psycopg2
from psycopg2.extras import RealDictCursor
import time


from . import models
from .database import engine
from .routers import post, user, auth, vote

from .config import settings

print(settings.database_username)

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

print("In fastapi-002")

while True:
    try:
        conn = psycopg2.connect(
            host="0.0.0.0",
            database="fastapi",
            user="postgres",
            password="password",
            cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        print ("Database connection was succesfull!!")
        break
    except Exception as error:
        print ("Connecting to databse failed")
        print("Error: ", error)
        time.sleep(2)

# list of dictionaries
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]    

@app.get("/")
def root():
    return {"message": "Hello World ..."}

