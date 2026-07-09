from fastapi import APIRouter
from src.db.models import User
from src.auth.dependencies import get_current_user
from .schemas import ReviewCreateModel
from src.db.main import get_session
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import ReviewService
from src.auth.dependencies import AccessTokenBearer

review_router = APIRouter()
review_service = ReviewService()
access_token_bearer = AccessTokenBearer()

@review_router.post('/book/{book_uid}')
async def add_review_to_book(
    book_uid: str,
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    new_review = await review_service.add_review_to_book(
        current_user.email,
        book_uid, review_data, session
    )
    
    return new_review
    

@review_router.get('/{review_uid}')
async def get_a_review(
    review_uid:str,
    token_details: dict = Depends(access_token_bearer),
    session: AsyncSession = Depends(get_session)
):
    review = await review_service.get_review_by_uid(review_uid, session)
    return review

