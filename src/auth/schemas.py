from pydantic import BaseModel
from sqlmodel import Field
import uuid
from datetime import datetime

class UserCreateModel(BaseModel):
    username: str = Field(max_length=8)
    email: str = Field(max_length=80)
    password: str = Field(min_length=8)
    first_name: str
    last_name: str
    
class UserResponse(BaseModel):
    uid : uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime 
    updated_at: datetime 
    