from fastapi import APIRouter, Depends, status
from .schemas import UserCreateModel, UserResponse, UserCredentials
from .service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from src.db.main import get_session
from .utils import verify_passwd, create_access_token, decode_token
from datetime import timedelta
from fastapi.responses import JSONResponse

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY_DAYS = 2

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    
    user_exists = await user_service.user_exists(email, session)
    
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'User with given email already exists.')
    else: 
        new_user = await user_service.create_user(user_data, session)
        
        return new_user

@auth_router.post('/signin')
async def user_signin(user_credentials: UserCredentials, session: AsyncSession = Depends(get_session)):
    email = user_credentials.email
    password = user_credentials.password
    user_exists = await user_service.user_exists(email, session)
    
    if user_exists:
        user = await user_service.get_user_by_email(email, session)
        password_valid = verify_passwd(user_credentials.password, user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data= {
                    'email': user.email,
                    'uid': str(user.uid)
                }
            )
            
            refresh_token = create_access_token(
                user_data={
                    'email': user.email,
                    'uid': str(user.uid)
                },
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS),
                refresh=True
            )
        
            return JSONResponse(
                content = {
                    "message": "login success",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user" : {
                        "email": user.email
                    }
                }
            )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")