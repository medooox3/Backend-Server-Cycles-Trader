from fastapi import APIRouter, Depends
from shared.models import UserRead, LicenseRead
from security.service import auth_service
from dependencies import DBSession
from ..service import profile_service

router = APIRouter()


@router.get("/", response_model=UserRead, description="Return this logged in user info")
async def me(user: UserRead = Depends(auth_service.get_user)):
    return user


@router.get("/license", response_model=LicenseRead)
async def get_license(
    session: DBSession, account_uuid: str, user: UserRead = Depends(auth_service.get_user)
):
    return profile_service.get_license(session, account_uuid)


@router.patch("/", response_model=UserRead)
async def change_profile_name(
    *,
    session: DBSession,
    user: UserRead = Depends(auth_service.get_user),
    name: str,
):
    return profile_service.change_profile_name(session, user, name)



@router.get("/ping")
async def ping(session: DBSession, user: UserRead = Depends(auth_service.get_user)):
    """call this api every 5 minutes to update the last seen status"""
    # Todo: udpate the last seen
    # access_session_utils.update_access_session_last_seen(session, access_session_uuid)
    profile_service.update_session_last_seen()
