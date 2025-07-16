from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

# Get current UTC time for demonstration
current_utc_time = datetime.now(timezone.utc)
print(current_utc_time)

class Post(Base):
    """SQLAlchemy model representing a blog post.

    Attributes:
        id (int): Unique identifier for the post.
        title (str): The title of the post.
        content (str): The content of the post.
        created_at (datetime): The creation timestamp of the post.
        author_id (int): Foreign key referencing the user who created the post.
        author (relationship): Relationship to the User model.
    """

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")