from fastapi import APIRouter

auth_router = APIRouter()

@auth_router.post('/signup')
async def user_signup():
    pass

@auth_router.post('/signin')
async def user_signin():
    pass