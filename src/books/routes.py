from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import List
from src.books.schemas import BookModel, BookUpdateModel
from src.books.book_data import books
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService

book_router = APIRouter()
book_service = BookService()

# get all books
@book_router.get('/')
async def get_all_books(session: AsyncSession = Depends(get_session)):
  books = await book_service.get_all_books(session)
  return books


# get a book by id
@book_router.get('/{book_uid}', response_model=BookModel)
async def get_a_book(book_uid: int, session: AsyncSession = Depends(get_session)) -> dict:
    retrieved_book = await book_service.get_a_book(book_uid, session)
    
    if retrieved_book:
        return retrieved_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Book not found.')
    

# Add a new book
@book_router.post('/', status_code=status.HTTP_201_CREATED, response_model=BookModel)
async def create_book(book_data: BookModel, session: AsyncSession = Depends(get_session)) -> dict:
  new_book = await book_service.create_book(new_book, session)
  return new_book


# update a book's data
@book_router.patch('/{book_uid}', response_model=BookModel)
async def update_book(book_uid: int, book_update_data:BookUpdateModel, session: AsyncSession = Depends(get_session)):
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Book to be updated NOT FOUND.')
    

@book_router.delete('/{book_uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: int, session: AsyncSession = Depends(get_session)):
    book_to_delete = await book_service.delete_book(book_uid, session)
    
    if book_to_delete:
        return None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Book to be deleted NOT FOUND.')
    
    