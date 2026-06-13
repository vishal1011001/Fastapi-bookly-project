from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc
from src.books.schemas import BookModel, BookCreateModel, BookUpdateModel


class BookService:
    def get_all_books(self, session:AsyncSession):
        statement = select(BookModel).order_by(desc(BookModel.created_at))
        result = await session.exec(statement)
        return result.all()
    
    def get_a_book(self, book_id:str, session:AsyncSession):
        statement = select(BookModel).where(BookModel.uid == book_id)
        result = await session.exec(statement)
        return result.first()
    
    def create_book(self, book_data:BookCreateModel, session:AsyncSession):
        book_data_dict = book_data.model_dump()
        await session.add(book_data_dict)
        await session.commit()
        return book_data_dict
    
    def update_book(self, book_id:str, book_update_data:BookUpdateModel, session:AsyncSession):
        book_to_update = self.get_a_book(book_id, session)
        update_data_dict = book_update_data.model_dump()
        
        for k, v in update_data_dict.items():
            setattr(book_to_update, k, v)
        
        await session.commit()
        return book_to_update
            
    def delete_book(self, book_id:str, session:AsyncSession):
        book_to_delete = self.get_a_book(book_id, session)
        
        await session.delete(book_to_delete)
        await session.commit()
        
        return {}
    