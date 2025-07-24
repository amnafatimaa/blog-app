from pydantic import BaseModel, constr
from datetime import datetime
from typing import Optional

class CommentBase(BaseModel):
    content: constr(min_length=1, strip_whitespace=True)

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    content: constr(min_length=1, strip_whitespace=True)

class CommentResponse(BaseModel):
    id: int
    content: str
    post_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
