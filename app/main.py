from ast import While
from sqlite3 import Cursor
from turtle import title
from typing import Optional
#from fastapi import Body, FastAPI

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

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for  i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello World ..."}

@app.get("/sqlalchemy")
def sqlalchemy(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return {"data": posts}

@app.get("/posts/{id}")
#def get_post(id: int, response: Response):
def get_post(id: int, db: Session = Depends(get_db)):
    print(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    print(post.__dict__)
    return{"post": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    print(id)
    delete_query = db.query(models.Post).filter(models.Post.id == id)

    if delete_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    delete_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post,  db: Session = Depends(get_db)):
    print("In Update")
    print(id)
    print(post)
    post_query = db.query(models.Post).filter(models.Post.id == id)

    db.commit()
    if post_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    updated_post = post_query.first()
    print(updated_post.__dict__)
    return{"post": updated_post}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

