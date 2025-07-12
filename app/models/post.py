from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

current_utc_time = datetime.now(timezone.utc)
print(current_utc_time)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")

users.posts = relationship("Post", back_populates="author")