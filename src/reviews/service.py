from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from .schemas import ReviewCreateModel
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

book_service = BookService()
user_service = UserService()

class ReviewService:
    
    async def add_review_to_book(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession
    ):
        try:
            book = await book_service.get_a_book(book_uid, session)
            user = await user_service.get_user_by_email(user_email, session)
            
            review_data_dict = review_data.model_dump()
            new_review = Review(
                **review_data_dict
            )
            
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found"
                )
                
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            new_review.user = user
            new_review.book = book
            
            session.add(new_review)
            await session.commit()
            return new_review
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server error at package service level."
            )
            
    async def get_review_by_uid(self, review_uid: str, session: AsyncSession):
        try:
            statement = select(Review).where(Review.uid == review_uid)
            review = await session.exec(statement)
            return review.first()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Review with given uid not found")
            
        