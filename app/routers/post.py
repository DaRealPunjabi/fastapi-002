from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/{id}", response_model=schemas.PostOut)
#def get_post(id: int, response: Response):
def get_post(id: int, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    print(id)
    print(current_user.__dict__)
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    print(post.__dict__)
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):

    print("In Delete")
    print(id)
    print(current_user.__dict__)
    delete_query = db.query(models.Post).filter(models.Post.id == id)

    delete_item = delete_query.first()

    if delete_item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    if delete_item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
    
    delete_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate,  db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    print("In Update")
    print(id)
    print(current_user.__dict__)
    print(post)

    update_query = db.query(models.Post).filter(models.Post.id == id)

    update_item = update_query.first()

    if update_item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if update_item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")

    update_query.update(post.dict(), synchronize_session=False)
    db.commit()
    updated_post = update_query.first()
    print(updated_post.__dict__)
    return updated_post

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user),
                 limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print("In Get")
    print(limit)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(
    #     limit).offset(skip).all()
    # posts = db.query(models.Post).limit(limit).all()
    # posts = db.query(models.Post).all()
    # posts = db.query(models.Post).filter(
    #     models.Post.owner_id == current_user.id).all()
    # print(type(posts))
    # for item in posts:
    #     print(item.__dict__)

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(
        limit).offset(skip).all()

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    print("In Create")
    print(current_user.__dict__)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
