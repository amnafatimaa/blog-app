from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """
    Base user model containing common user attributes that are shared across different user schemas.
    
    Attributes:
        username: The username for the user account.
        email: The email address for the user (validated as a proper email format).
    """
    username: str
    email: EmailStr  # Uses Pydantic's EmailStr for email validation

class UserCreate(UserBase):
    """
    Schema for creating a new user. Extends UserBase with password field.
    Used for user registration/creation endpoints.
    
    Attributes:
        password: The plain-text password for the new user account.
    """
    password: str  # Note: In production, this should never be stored or returned in responses

class User(UserBase):
    """
    Complete user schema including database ID. Used for returning user data in responses.
    Inherits all fields from UserBase and adds the user ID.
    
    Attributes:
        id: The unique database identifier for the user.
    """
    id: int
    
    class Config:
        """
        Pydantic configuration to enable ORM mode.
        This allows the model to read data directly from SQLAlchemy ORM objects.
        """
        from_attributes = True  # Enables compatibility with ORMs like SQLAlchemy
