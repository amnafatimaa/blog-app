from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema
import secrets
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configuration from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def verify_password(plain_password: str, hashed_password: str):
    """Verifies a plain password against a hashed password.

    Args:
        plain_password (str): The unhashed password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    # Verify the plain password against the hashed version
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    """Generates a hash for the given password.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    # Hash the provided password
    return pwd_context.hash(password)

def create_access_token(data: dict):
    """Creates a JWT access token with an expiration time.

    Args:
        data (dict): The data to encode in the token (e.g., user info).

    Returns:
        str: The encoded JWT token.

    Raises:
        Exception: If JWT encoding fails due to invalid SECRET_KEY or data.
    """
    # Create a copy of the data and add expiration
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Encode the token with the secret key and algorithm
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Retrieves the current user based on a JWT token.

    Args:
        token (str): The JWT token from the request.
        db (Session): Database session for user query.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: If the token is invalid or user is not found (status code 401).
    """
    # Define exception for invalid credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token and extract username
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # Query the user from the database
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
