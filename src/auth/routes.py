from fastapi import APIRouter, Depends, status
from .schemas import UserCreateModel, UserResponse
from .service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException

auth_router = APIRouter()
user_service = UserService()

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends()):
    email = user_data.email
    
    user_exists = await user_service.user_exists(email)
    
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'User with given email already exists.')
    else: 
        new_user = await user_service.create_user(user_data, session)
        
        return new_user

@auth_router.post('/signin')
async def user_signin():
    pass