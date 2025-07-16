from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.post import Post, PostCreate
from app.crud.post import create_post, get_posts, get_post, update_post, delete_post
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=Post)
def create_new_post(post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_post(db, post, current_user.id)

@router.get("/", response_model=List[Post])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_posts(db, skip, limit)

@router.get("/{post_id}", response_model=Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=Post)
def update_existing_post(post_id: int, post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_post = get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    updated_post = update_post(db, post_id, post)
    return updated_post

@router.delete("/{post_id}")
def delete_existing_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_post = get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    delete_post(db, post_id)
    return {"message": "Post deleted"}