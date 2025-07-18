from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    """SQLAlchemy model representing a user.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): The unique username of the user.
        email (str): The unique email address of the user.
        hashed_password (str): The hashed password for user authentication.
        posts: Relationship to Post model, representing all posts authored by the user.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    posts = relationship("Post", back_populates="author")
