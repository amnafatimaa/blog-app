from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Post(Base):
    """SQLAlchemy model representing a blog post.

    Attributes:
        id (int): Unique identifier for the post.
        title (str): The title of the post.
        content (str): The content of the post.
        created_at (datetime): The creation timestamp of the post.
        author_id (int): Foreign key referencing the user who created the post.
        author (relationship): Relationship to the User model.
        comments (relationship): Relationship to the Comment model.
    """

    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")