from sqlalchemy.orm import Session
from app.models.comments import Comment
from datetime import datetime

def create_comment(db: Session, content: str, post_id: int, user_id: int):
    new_comment = Comment(content=content, post_id=post_id, user_id=user_id)
    if new_comment:
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment

def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()

def get_comments_by_post(db:Session, post_id: int, skip: int = 0, limit: int = 100):
    return db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()

def update_comment(db: Session, comment_id: int, content: str):
    if not content.strip():
        raise ValueError("comment content cannot be empty")
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        return None
    comment.content = content
    comment.updated_at = datetime.utcnow()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise
    db.refresh(comment)
    return comment
    

def delete_comment(db: Session, comment_id: int):
    """Deletes a comment from the database by its ID.

    Args:
        db (Session): Database session.
        comment_id (int): ID of the comment to delete.

    Raises:
        Exception: If the deletion fails (e.g., due to database constraints).
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
        db.refresh()
        return "Comment has been deleted"