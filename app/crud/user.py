from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.dependencies.auth import get_password_hash

def create_user(db: Session, user: UserCreate):
    """Creates a new user in the database with a hashed password.

    Args:
        db (Session): Database session for transaction management.
        user (UserCreate): Schema containing user data to create.

    Returns:
        User: The created user object.

    Raises:
        Exception: If database operations fail (e.g., integrity errors).
    """
    # Hash the user's password for security
    hashed_password = get_password_hash(user.password)
    # Create a new user instance with hashed password
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    """Retrieves a user by their username.

    Args:
        db (Session): Database session for query execution.
        username (str): The username to search for.

    Returns:
        User: The user object if found, None otherwise.
    """
    # Query the user by their username
    return db.query(User).filter(User.username == username).first()
