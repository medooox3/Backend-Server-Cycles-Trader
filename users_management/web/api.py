from fastapi import APIRouter
from sqlmodel import select, delete, update
from ..data import User, License
from di import get_session, DBSession

router = APIRouter()


@router.post("/", response_model=User)
def create_user(*, session: DBSession, user: User) -> User:
    # Todo: before creating a user check if the user already exists
    # Also decide whether to create a license before creating him or after he is created 
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/", response_model=list[User])
def get_users(session: DBSession):
    users = session.exec(select(User)).all()
    return users
