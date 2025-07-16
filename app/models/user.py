from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    """SQLAlchemy model representing a user.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): The unique username of the user.
        email (str): The unique email address of the user.
        hashed_password (str): The hashed password for user authentication.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)