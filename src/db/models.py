from sqlmodel import SQLModel, Field, Column, Relationship
from typing import List, Optional
from src.books import models
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
import uuid

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
    books: List[Book] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    
    def __repr__(self):
        return f"<user {self.username}>"
    

class Book(SQLModel, table=True):
    __tablename__ = "books"
    
    uid: uuid.UUID = Field(
        sa_column = Column(
            pg.UUID,
            nullable = False,
            primary_key = True,
            default = uuid.uuid4
        )
    ) 
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key='users.uid')
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional[User] = Relationship(back_populates="books")
    
    def __repr__(self):
        return f"<book {self.title}>"
    
    
class Review(SQLModel, table=True):
    __tablename__="reviews"
    
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    rating: int = Field(lt=6)
    review_text: str
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    def __repr__(self):
        return f"<Review of book {Book.uid} by user {User.uid}>"
    