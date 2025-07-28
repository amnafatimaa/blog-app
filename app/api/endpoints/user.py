from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import User, UserCreate
from app.crud.user import create_user, get_user_by_username
from app.dependencies.auth import create_access_token, verify_password
from app.schemas.token import TokenData
from app.core.config import settings
import jwt

router = APIRouter(prefix="/users", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Registers a new user with the provided details.

    Args:
        user (UserCreate): The user data to be registered.
        db (Session): Database session dependency.

    Returns:
        User: The created user object.

    Raises:
        HTTPException: If the username is already registered (status code 400).
    """
    # Check if the username is already taken
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    # Create and save the new user
    return create_user(db, user)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticates a user and returns an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing username and password.
        db (Session): Database session dependency.

    Returns:
        dict: A dictionary containing the access token and token type.

    Raises:
        HTTPException: If the username or password is incorrect (status code 401).
    """
    # Retrieve user and verify credentials
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Generate and return access token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    print(f"Received token: {token[:50]}...")  # Debug: print first 50 chars
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(f"Decoded payload: {payload}")  # Debug: print payload
        
        username: str = payload.get("sub")
        if username is None:
            print("No username in token payload")  # Debug
            raise credentials_exception
        token_data = TokenData(username=username)
        
    except jwt.PyJWTError as e:
        print(f"JWT decode error: {e}")  # Debug: print specific error
        raise credentials_exception

    user = get_user_by_username(db, username)
    if user is None:
        print(f"User not found: {username}")  # Debug
        raise credentials_exception
    
    print(f"Authentication successful for user: {username}")  # Debug
    return user

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    """Returns the current user's profile.

    Args:
        current_user (User): The authenticated user.

    Returns:
        User: The user object.
    """
    return current_user
