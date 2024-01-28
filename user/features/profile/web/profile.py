from fastapi import APIRouter, Depends
from users_management.data import UserRead, LicenseRead
from security.web import auth_api
from dependencies import DBSession
from admin.features.users_management.service import users_service
from admin.features.users_management.service import accounts_service


router = APIRouter()


@router.get("/", response_model=UserRead, description="Return this logged in user info")
async def me(user: UserRead = Depends(auth_api.get_user)):
    return user


@router.get("/license", response_model=LicenseRead)
async def get_license(
    session: DBSession, account_uuid: str, user: UserRead = Depends(auth_api.get_user)
):
    account = accounts_service.get_account_from_uuid(session, account_uuid)
    return users_service.get_account_license(session, account.id)  # type: ignore


@router.patch("/", response_model=UserRead)
async def change_profile_name(
    *,
    session: DBSession,
    user: UserRead = Depends(auth_api.get_user),
    name: str,
):
    return users_service.change_profile_name(session, user.id, name)


# Todo: Use client side state management to keep track of the active account
# @router.post("/switch")
# async def switch_account(account_uuid: str, response: Response):
#     """change the current active account"""
#     response.set_cookie(key="account", value=account_uuid, httponly=True)


@router.get("/ping")
async def ping(session: DBSession, user: UserRead = Depends(auth_api.get_user)):
    """call this api every 5 minutes to update the last seen status"""
    # Todo: udpate the last seen
    # access_session_utils.update_access_session_last_seen(session, access_session_uuid)
    pass
