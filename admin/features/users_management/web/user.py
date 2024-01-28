from fastapi import APIRouter, status
from ..data import User, UserCreate, UserRead, UserUpdate, UserSearch
from ..service import users_service

# from security.utils import password_utils
from dependencies import DBSession
from .user_license import router as license_router
# from .user_cycles import router as cycles_router
from .user_accounts import router as accounts_router


router = APIRouter(tags=["Users Management"])
router.include_router(license_router, prefix="/licenses")
# router.include_router(cycles_router, prefix="/cycles")
router.include_router(accounts_router, prefix="/accounts")


# * --------------- Users ------------- *
@router.post("/", response_model=UserRead)
async def create_user(*, session: DBSession, user_in: UserCreate):
    return users_service.create_user(session, user_in)


@router.patch("/", response_model=UserRead)
async def update_user(*, session: DBSession, id: int, user_in: UserUpdate):
    return users_service.update_user(session, id, user_in)


# Todo: expose later for users
async def update_user_password(*, session: DBSession, user_id: int, new_password: str):
    users_service.change_password(session, user_id, new_password)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(session: DBSession, user_id: int):
    users_service.delete_user(session, user_id)


@router.get("/", response_model=list[UserRead])
async def get_users(session: DBSession):
    return users_service.get_all_users(session)


@router.post("/find/", response_model=UserRead)
async def get_user(session: DBSession, filter: UserSearch):
    return users_service.find_user_using_filter(session, filter)
    # Create a model similar to the update model, and have attributes that are
    # optional like: name, email, phone, location, uuid, id to find the user
    pass
