from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import User, UserCreate
from app.crud.user import create_user, get_user_by_username
from app.dependencies.auth import create_access_token, verify_password

router = APIRouter(prefix="/users", tags=["users"])

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
