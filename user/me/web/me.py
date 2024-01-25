from typing import Annotated
from fastapi import APIRouter, Depends, Query
from users_management.data import user_repo, UserRead, UserUpdate, LicenseRead
from security.web import auth_api

from di import DBSession


router = APIRouter()


@router.get("/", response_model=UserRead, description="Return this logged in user info")
async def me(user: UserRead = Depends(auth_api.get_user)):
    return user


@router.get("/license", response_model=LicenseRead)
async def get_license(session: DBSession, user: UserRead = Depends(auth_api.get_user)):
    return user_repo.get_user_license(session, user.id)


@router.patch("")
async def change_profile_name(
    session: DBSession,
    user: UserRead = Depends(auth_api.get_user),
    name: str = Query(),
):
    user_repo.change_profile_name(session, user.id, name)
