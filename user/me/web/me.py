from fastapi import APIRouter, Depends
from users_management.data import user_repo, UserRead, UserUpdate
from security.web import auth_api

router = APIRouter()


@router.get("/", response_model=UserRead, description='Return this logged in user info')
async def me(user: UserRead = Depends(auth_api.get_user)):
    return user


