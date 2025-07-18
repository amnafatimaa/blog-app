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
    """Creates a new post for the authenticated user.

    Args:
        post (PostCreate): The post data to be created.
        db (Session): Database session dependency.
        current_user (User): The authenticated user creating the post.

    Returns:
        Post: The created post object.

    Raises:
        HTTPException: If there’s an issue with database operations.
    """
    # Create a new post with the provided data and user ID
    return create_post(db, post, current_user.id)

@router.get("/", response_model=List[Post])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Retrieves a list of posts with pagination.

    Args:
        skip (int): Number of posts to skip (default: 0).
        limit (int): Maximum number of posts to return (default: 10).
        db (Session): Database session dependency.

    Returns:
        List[Post]: A list of post objects.

    Raises:
        HTTPException: If there’s an issue with database operations.
    """
    # Fetch posts with the specified skip and limit
    return get_posts(db, skip, limit)

@router.get("/{post_id}", response_model=Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific post by its ID.

    Args:
        post_id (int): The ID of the post to retrieve.
        db (Session): Database session dependency.

    Returns:
        Post: The requested post object.

    Raises:
        HTTPException: If the post is not found (status code 404).
    """
    # Retrieve post by ID and check if it exists
    post = get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=Post)
def update_existing_post(post_id: int, post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Updates an existing post if the user is authorized.

    Args:
        post_id (int): The ID of the post to update.
        post (PostCreate): The updated post data.
        db (Session): Database session dependency.
        current_user (User): The authenticated user requesting the update.

    Returns:
        Post: The updated post object.

    Raises:
        HTTPException: If the post is not found (404) or user is not authorized (403).
    """
    # Fetch the post and verify it exists
    db_post = get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    # Check if the current user is the author
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    # Update the post with new data
    updated_post = update_post(db, post_id, post)
    return updated_post

@router.delete("/{post_id}")
def delete_existing_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Deletes an existing post if the user is authorized.

    Args:
        post_id (int): The ID of the post to delete.
        db (Session): Database session dependency.
        current_user (User): The authenticated user requesting the deletion.

    Returns:
        dict: A message confirming the deletion.

    Raises:
        HTTPException: If the post is not found (404) or user is not authorized (403).
    """
    # Fetch the post and verify it exists
    db_post = get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    # Check if the current user is the author
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    # Delete the post from the database
    delete_post(db, post_id)
    return {"message": "Post deleted"}
