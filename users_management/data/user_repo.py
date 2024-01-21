from typing import Optional
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from security.utils import password_utils
from .user import UserCreate, User, UserSearch, UserUpdate


UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
)


def _map_user(user: UserCreate) -> User:
    """Convert UserCreate to User"""
    return User(
        name=user.name,
        email=user.email,
        location=user.location,
        phone=user.phone,
        password_hash=password_utils.get_password_hash(user.password),
    )


def create_user(session: Session, user: UserCreate) -> User:
    # Todo: raise exceptions if user is found in the DB or any attribute is not unique
    db_user = _map_user(user)
    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exist: name, email, phone must be unique")


def find_user_using_filter(session: Session, filter: UserSearch) -> User:
    user: Optional[User]

    if filter.id:
        user = session.get(User, filter.id)

    elif filter.uuid:
        user = session.exec(select(User).where(User.uuid == filter.uuid)).first()

    elif filter.name:
        user = session.exec(select(User).where(User.name == filter.name)).first()

    elif filter.email:
        user = session.exec(select(User).where(User.email == filter.email)).first()

    elif filter.phone:
        user = session.exec(select(User).where(User.phone == filter.phone)).first()

    else:
        user = None

    if not user:
        raise UserNotFoundException

    return user


def delete_user(session: Session, filter: UserSearch):
    user = find_user_using_filter(session, filter)
    session.delete(user)
    session.commit()


def update_user(session: Session, id: int, user: UserUpdate):
    db_user = session.get(User, id)

    if not db_user:
        raise UserNotFoundException

    for field, value in user.model_dump(exclude_unset=True).items():
        if field == "password":
            field = "password_hash"
            value = password_utils.get_password_hash(value)
        setattr(db_user, field, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def change_password(session: Session, user_id: int, new_password: str):
    db_user = session.get(User, user_id)

    if not db_user:
        raise UserNotFoundException

    db_user.password_hash = password_utils.get_password_hash(new_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
