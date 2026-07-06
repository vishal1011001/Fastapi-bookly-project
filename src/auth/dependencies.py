from fastapi.security import HTTPBearer
from fastapi import Request, status, Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from fastapi.exceptions import HTTPException
from src.db.redis import token_exists_in_blocklist
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import UserService
from .models import User

user_service = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        
        token = creds.credentials
        token_data = decode_token(token)
        
        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                        'error': "Token is invalid",
                        'resolution': "Please get a new token"
                    }
            )
        
        # check for revoked token
        if await token_exists_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                        'error': "Token is expired or revoked",
                        'resolution': "Please get a new token"
                    }
            )
        
        self.verify_token_data(token_data)
        
        return token_data
    
    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        return token_data is not None
    
    def verify_token_data(self, token_data):
        raise NotImplementedError("Override this method in child classes.")
    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict):
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Provide an access token."
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict):
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Provide an refresh token."
            )
            

async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session)
):
    email = token_details['user']['email']
    user = await user_service.get_user_by_email(email, session)
    
    return user


class RoleChecker:
    def __init__(self, allowed_roles: list[str]) -> None:
        self.allowed_roles = allowed_roles
        
    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role in self.allowed_roles:
            return True
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to access this endpoint."
        )
    