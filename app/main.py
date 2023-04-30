from ast import While
from sqlite3 import Cursor
from turtle import title
from typing import List, Optional
from typing_extensions import deprecated
#from fastapi import Body, FastAPI

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

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

