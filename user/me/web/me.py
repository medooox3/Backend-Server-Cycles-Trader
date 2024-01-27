from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response, Request
from users_management.data import user_repo, UserRead, UserUpdate, LicenseRead
from security.web import auth_api
from security.utils import access_session_utils
from di import DBSession


router = APIRouter()


@router.get("/", response_model=UserRead, description="Return this logged in user info")
async def me(user: UserRead = Depends(auth_api.get_user)):
    return user


@router.get("/license", response_model=LicenseRead)
async def get_license(
    session: DBSession, account_uuid: str, user: UserRead = Depends(auth_api.get_user)
):
    account = user_repo.get_account_from_uuid(session, account_uuid)
    return user_repo.get_account_license(session, account.id)  # type: ignore


@router.patch("/", response_model=UserRead)
async def change_profile_name(
    *,
    session: DBSession,
    user: UserRead = Depends(auth_api.get_user),
    name: str,
):
    return user_repo.change_profile_name(session, user.id, name)


@router.post("/switch")
async def switch_account(account_uuid: str, response: Response):
    """change the current active account"""
    response.set_cookie(key="account", value=account_uuid, httponly=True)


@router.get("/ping")
async def ping(session: DBSession, user: UserRead = Depends(auth_api.get_user)):
    """call this api every 5 minutes to update the last seen status"""
    # Todo: udpate the last seen
    # access_session_utils.update_access_session_last_seen(session, access_session_uuid)
    pass
