from pydantic import BaseModel
from datetime import datetime
from sqlmodel import Field
from typing import Optional
import uuid


class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int = Field(lt=6)
    review_text: str 
    user_uid: Optional[uuid.UUID]
    book_uid: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime
    

class ReviewCreateModel(BaseModel):
    rating: int = Field(lt=6)
    review_text: str