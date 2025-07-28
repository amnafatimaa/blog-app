from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.dependencies.auth import get_password_hash

def create_user(db: Session, user: UserCreate):
    """Creates a new user in the database with hashed password.

    Args:
        db (Session): Database session for transaction management.
        user (UserCreate): Schema containing user data to create.

    Returns:
        User: The created user object.

    Raises:
        Exception: If database operations fail (e.g., integrity errors).
    """
    hashed_password = get_password_hash(user.password)
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
    return db.query(User).filter(User.username == username).first()