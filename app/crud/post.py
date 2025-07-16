from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate

def create_post(db: Session, post: PostCreate, user_id: int):
    """Creates a new post in the database.

    Args:
        db (Session): Database session for transaction management.
        post (PostCreate): Schema containing post data to create.
        user_id (int): ID of the user creating the post.

    Returns:
        Post: The created post object.

    Raises:
        Exception: If database operations fail (e.g., integrity errors).
    """
    # Create a new post instance with provided data and user ID
    db_post = Post(**post.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 10):
    """Retrieves a list of posts with optional pagination.

    Args:
        db (Session): Database session for query execution.
        skip (int, optional): Number of posts to skip. Defaults to 0.
        limit (int, optional): Maximum number of posts to return. Defaults to 10.

    Returns:
        List[Post]: A list of post objects.
    """
    # Query posts with offset and limit for pagination
    return db.query(Post).offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int):
    """Retrieves a specific post by its ID.

    Args:
        db (Session): Database session for query execution.
        post_id (int): The ID of the post to retrieve.

    Returns:
        Post: The post object if found, None otherwise.
    """
    # Query the post by its ID
    return db.query(Post).filter(Post.id == post_id).first()

def update_post(db: Session, post_id: int, post: PostCreate):
    """Updates an existing post with new data.

    Args:
        db (Session): Database session for transaction management.
        post_id (int): The ID of the post to update.
        post (PostCreate): Schema containing updated post data.

    Returns:
        Post: The updated post object if found, None otherwise.
    """
    # Fetch the post and update its attributes if it exists
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        for key, value in post.dict().items():
            setattr(db_post, key, value)
        db.commit()
        db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    """Deletes a specific post by its ID.

    Args:
        db (Session): Database session for transaction management.
        post_id (int): The ID of the post to delete.

    Returns:
        Post: The deleted post object if found, None otherwise.
    """
    # Fetch the post and delete it if it exists
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post