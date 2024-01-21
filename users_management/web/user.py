from fastapi import APIRouter, status
from sqlmodel import select
from ..data import User, UserCreate, UserRead, UserUpdate, License, UserSearch
from ..data import user_repo
# from security.utils import password_utils
from di import DBSession
from .user_license import router as user_license_router

router = APIRouter(tags=["Users Management"])
router.include_router(user_license_router)

# * --------------- Users ------------- *
@router.post("/", response_model=UserRead)
def create_user(*, session: DBSession, user_in: UserCreate):
    return user_repo.create_user(session, user_in)


@router.patch("/", response_model=UserRead)
def update_user(*, session: DBSession, id: int, user_in: UserUpdate):
    return user_repo.update_user(session, id, user_in)


# Todo: expose later for users
def update_user_password(*, session: DBSession, user_id: int, new_password: str):
    user_repo.change_password(session, user_id, new_password)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(session: DBSession, filter: UserSearch):
    user_repo.delete_user(session, filter)


@router.get("/", response_model=list[UserRead])
def get_users(session: DBSession):
    return user_repo.get_all_users(session)


@router.post("/find/", response_model=UserRead)
def get_user(session: DBSession, filter: UserSearch):
    return user_repo.find_user_using_filter(session, filter)
    # Create a model similar to the update model, and have attributes that are
    # optional like: name, email, phone, location, uuid, id to find the user
    pass


# * ------------------ License ------------------- *
def create_license():
    # select the user and link license to user
    pass


def update_license():
    # update the license
    pass


def delete_license():
    # delete the license
    pass


def get_licenses():
    # return all licenses for all users (show license id, user id, user name, expire date)
    pass


def get_license():
    #  return the licese for a user
    pass
