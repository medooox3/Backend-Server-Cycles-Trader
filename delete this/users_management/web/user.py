from fastapi import APIRouter, status
from sqlmodel import select
from ..data import User, UserCreate, UserRead, UserUpdate, License, UserSearch
from ..data import user_service

# from security.utils import password_utils
from dependencies import DBSession
from .user_license import router as user_license_router
from .user_cycles import router as user_cycles_router


router = APIRouter(tags=["Users Management"])
router.include_router(user_license_router)
router.include_router(user_cycles_router)


# * --------------- Users ------------- *
@router.post("/", response_model=UserRead)
async def create_user(*, session: DBSession, user_in: UserCreate):
    return user_service.create_user(session, user_in)


@router.patch("/", response_model=UserRead)
async def update_user(*, session: DBSession, id: int, user_in: UserUpdate):
    return user_service.update_user(session, id, user_in)


# Todo: expose later for users
async def update_user_password(*, session: DBSession, user_id: int, new_password: str):
    user_service.change_password(session, user_id, new_password)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(session: DBSession, filter: UserSearch):
    user_service.delete_user(session, filter)


@router.get("/", response_model=list[UserRead])
async def get_users(session: DBSession):
    return user_service.get_all_users(session)


@router.post("/find/", response_model=UserRead)
async def get_user(session: DBSession, filter: UserSearch):
    return user_service.find_user_using_filter(session, filter)
    # Create a model similar to the update model, and have attributes that are
    # optional like: name, email, phone, location, uuid, id to find the user
    pass
