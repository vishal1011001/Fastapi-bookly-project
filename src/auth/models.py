from sqlmodel import SQLModel, Field, Column, Relationship
from typing import List
from src.books import models
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime, date

class User(SQLModel, table=True):
    __tablename__ = 'users'
    
    uid : uuid.UUID = Field(
        sa_column = Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(sa_column=Column(
        pg.VARCHAR,
        nullable=False,
        server_default="user"
    ))
    is_verified: bool = Field(sa_column=Column(pg.BOOLEAN, default=False))
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List["models.Book"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    
    def __repr__(self):
        return f"<user {self.username}>"