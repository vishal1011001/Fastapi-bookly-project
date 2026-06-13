from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from typing import List
from src.books.schemas import BookModel, BookUpdateModel
from src.books.book_data import books

book_router = APIRouter()

# get all books
@book_router.get('/', response_model = List[BookModel])
async def get_all_books():
  return books


# get a book by id
@book_router.get('/{book_id}')
async def get_a_book(book_id: int) -> dict:
    for book in books:
        if book['id'] == book_id:
            return book
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Book not found.'
                        )
    

# Add a new book
@book_router.post('/', status_code=status.HTTP_201_CREATED, response_model=BookModel)
async def create_book(book_data: BookModel) -> dict:
  new_book = book_data.model_dump()
  books.append(new_book)
  return new_book


# update a book's data
@book_router.patch('/{book_id}')
async def update_book(book_id: int, book_data:BookUpdateModel):
    for book in books:
        if book['id'] == book_id:
            book['title'] = book_data.title
            book['author'] = book_data.author
            book['publisher'] = book_data.publisher
            book['published_date'] = book_data.published_date
            book['page_count'] = book_data.page_count
            book['language'] = book_data.language
            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Book to be updated NOT FOUND.')
    

@book_router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return {}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Book to be deleted NOT FOUND.')
    
    