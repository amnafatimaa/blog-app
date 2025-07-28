from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.user import User  # Import your existing User schema

class PostBase(BaseModel):
    """Base Pydantic model for common post attributes.

    Attributes:
        title (str): The title of the post.
        content (str): The content of the post.
    """

    title: str
    content: str

class PostCreate(PostBase):
    """Pydantic model for creating a new post, inheriting from PostBase.

    Attributes:
        Inherits all fields from PostBase.
    """
    pass

class Post(PostBase):
    """Pydantic model for a full post, including database-generated fields.

    Attributes:
        id (int): The unique identifier of the post.
        created_at (datetime): The creation timestamp of the post.
        author_id (int): The ID of the user who created the post.
        author (User): The user who created the post (ONLY NEW FIELD ADDED).
        Inherits title and content from PostBase.

    Config:
        from_attributes (bool): Enables ORM mode for compatibility with SQLAlchemy models.
    """

    id: int
    created_at: datetime
    author_id: int
    author: Optional[User] = None  # ONLY ADD THIS ONE LINE

    class Config:
        from_attributes = True