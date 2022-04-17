from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from .. import models, schema
from ..database import get_db
from typing import List

router = APIRouter(
    prefix='/posts',
    tags=['posts']
)


@router.get('/', response_model=List[schema.Post])
def posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.get('/{id}', response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            detail=f'post with {id} not found', status_code=status.HTTP_404_NOT_FOUND)

    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put('/id}', status_code=status.HTTP_202_ACCEPTED, response_model=schema.Post)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(
            detail=f'post with {id} not found', status_code=status.HTTP_404_NOT_FOUND)

    post.update(updated_post.dict())
    db.commit()
    return post.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(
            detail=f'post with {id} not found', status_code=status.HTTP_404_NOT_FOUND)

    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
