from fastapi import APIRouter, Depends, status
from .schemas import UserCreateModel, UserResponse, UserCredentials, UserBookModel
from .service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from src.db.main import get_session
from .utils import verify_passwd, create_access_token
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.db.redis import add_jti_to_blocklist

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(['admin', 'user'])

REFRESH_TOKEN_EXPIRY_DAYS = 2

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user_account(
    user_data: UserCreateModel, 
    session: AsyncSession = Depends(get_session)
):
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
 
   
@auth_router.get('/refresh_token')
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    """Get new access token using valid refresh token"""
    
    expiry_timestamp = token_details['exp']
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details['user']
        )
        
        return JSONResponse(content={
            'access_token': new_access_token
        })
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail="Invalid or expired token.")
    
@auth_router.get('/me', response_model=UserBookModel)
async def get_current_user(
    user = Depends(get_current_user),
    _:bool = Depends(role_checker)
):
    return user

@auth_router.post('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']
    await add_jti_to_blocklist(jti)
    
    return JSONResponse(
        content={
            'message': 'Logged out successfully.'
        },
        status_code=status.HTTP_200_OK
    )