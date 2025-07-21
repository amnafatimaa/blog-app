from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.comments import CommentCreate, CommentResponse, CommentUpdate  
from app.crud.comments import create_comment, get_comments_by_post, get_comment, update_comment, delete_comment  
from app.crud.post import get_post
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/comments", tags=["comments"]) 

@router.post("/{post_id}/comments/", response_model=CommentResponse)
def create_new_comment(
    post_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ):
    """Creates a new comment for a specific post by the authenticated user.

    Args:
        post_id (int): The ID of the post to comment on.
        comment (CommentCreate): The comment data to be created.
        db (Session): Database session dependency.
        current_user (User): The authenticated user creating the comment.

    Returns:
        CommentResponse: The created comment object.

    Raises:
        HTTPException: If there’s an issue with database operations or if the post does not exist.
    """
    return create_comment(db, comment.content, post_id, current_user.id)

@router.get("/{post_id}/comments/", response_model=List[CommentResponse])
def read_comments(
    post_id: int, 
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
    ):
    """Retrieves a list of comments for a specific post with pagination.

    Args:
        post_id (int): The ID of the post to retrieve comments for.
        skip (int): Number of comments to skip (default: 0).
        limit (int): Maximum number of comments to return (default: 10).
        db (Session): Database session dependency.

    Returns:
        List[CommentResponse]: A list of comment objects for the specified post.

    Raises:
        HTTPException: If there’s an issue with database operations or if the post does not exist.
    """
    comments = get_comments_by_post(db, post_id, skip, limit)
    if not comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No comments found for this post")
    return comments

@router.get("/{post_id}/comments/{comment_id}", response_model=CommentResponse)
def get_specific_comment(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves a specific comment for a post if the authenticated user is either the comment creator or the post creator.

    Args:
        post_id (int): The ID of the post the comment belongs to.
        comment_id (int): The ID of the comment to retrieve.
        db (Session): Database session dependency.
        current_user (User): The authenticated user attempting to retrieve the comment.

    Returns:
        CommentResponse: The requested comment object.

    Raises:
        HTTPException:
            - 404: If the post or comment does not exist.
            - 403: If the user is not authorized to view the comment.
    """
    # Check if the comment exists
    comment = get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    # Verify that the comment belongs to the specified post
    if comment.post_id != post_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Comment does not belong to the specified post")

    # Check if the post exists and get the post creator
    post = get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return comment

@router.put("/{post_id}/comments/{comment_id}", response_model=CommentResponse)
def update_existing_comment(
    post_id: int,
    comment_id: int,
    comment_update: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Updates a comment's content if the authenticated user is either the comment creator or the post creator.

    Args:
        post_id (int): The ID of the post the comment belongs to.
        comment_id (int): The ID of the comment to update.
        comment_update (CommentUpdate): The updated comment data.
        db (Session): Database session dependency.
        current_user (User): The authenticated user attempting to update the comment.

    Returns:
        CommentResponse: The updated comment object.

    Raises:
        HTTPException:
            - 404: If the post or comment does not exist.
            - 403: If the user is not authorized to update the comment.
            - 500: If a database error occurs during update.
    """
    comment = get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if comment.post_id != post_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Comment does not belong to the specified post")
    post = get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if current_user.id not in (comment.user_id, post.author_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this comment")
    updated_comment = update_comment(db, comment_id, comment_update.content)
    if not updated_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found during update")
    return updated_comment

@router.delete("/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_comment(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deletes a comment if the authenticated user is either the comment creator or the post creator.

    Args:
        post_id (int): The ID of the post the comment belongs to.
        comment_id (int): The ID of the comment to delete.
        db (Session): Database session dependency.
        current_user (User): The authenticated user attempting to delete the comment.

    Returns:
        None: Returns a 204 No Content status code on successful deletion.

    Raises:
        HTTPException:
            - 404: If the post or comment does not exist.
            - 403: If the user is not authorized to delete the comment.
            - 500: If a database error occurs during deletion.
    """
    # Check if the comment exists
    comment = get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    # Verify that the comment belongs to the specified post
    if comment.post_id != post_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Comment does not belong to the specified post")

    # Check if the post exists and get the post creator
    post = get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # Check if the current user is either the comment creator or the post creator
    if current_user.id not in (comment.user_id, post.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this comment")

    # Delete the comment
    try:
        delete_comment(db, comment_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete comment: {str(e)}")

    return None