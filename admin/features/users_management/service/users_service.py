from typing import Optional
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from security.service import password_service
from ..data import (
    UserCreate,
    User,
    UserSearch,
    UserUpdate,
)
from ..data.exceptions import (
    UserNotFoundException,
    UserAlreadyExists,
)
from . import license_service


def _map_user(user: UserCreate) -> User:
    """Convert UserCreate to User"""
    return User(
        # Lower, so that no same user name can be created (ex: ali, Ali)
        name=user.name.lower(),
        email=user.email,
        location=user.location,
        phone=user.phone,
        password_hash=password_service.get_password_hash(user.password),
    )


def get_user(session: Session, user_id: int) -> Optional[User]:
    """get user by db id"""
    return session.get(User, user_id)


def get_user_by_name(session: Session, name: str) -> Optional[User]:
    """search for user by name"""
    return session.exec(select(User).where(User.name == name)).first()


def get_all_users(session: Session) -> list[User]:
    """Get all registered users"""
    return list(session.exec(select(User)).all())


def create_user(session: Session, user: UserCreate) -> User:
    """Create new user, if `username`, `email` or the `phone` is already
    registered to another user, creating this user will not be possible."""
    db_user = _map_user(user)
    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except IntegrityError:
        raise UserAlreadyExists


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

    elif filter.license_id:
        user = license_service.get_user_of_license(session, filter.license_id)
    else:
        user = None

    if not user:
        raise UserNotFoundException

    return user


# def delete_user(session: Session, filter: UserSearch):
# user = find_user_using_filter(session, filter)
def delete_user(session: Session, user_id: int):
    user = get_user(session, user_id)
    if not user:
        raise UserNotFoundException

    # Find and delete all related objects (licenses and accounts)
    if user.licenses is not None:
        for license in user.licenses:
            session.delete(license)
    if user.accounts is not None:
        for account in user.accounts:
            session.delete(account)

    # Delete the user
    session.delete(user)

    session.commit()


def update_user(session: Session, id: int, user: UserUpdate):
    db_user = session.get(User, id)

    if not db_user:
        raise UserNotFoundException

    for field, value in user.model_dump(exclude_unset=True).items():
        if field == "password":
            field = "password_hash"
            value = password_service.get_password_hash(value)
        setattr(db_user, field, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def change_password(session: Session, user_id: int, new_password: str):
    db_user = session.get(User, user_id)

    if not db_user:
        raise UserNotFoundException

    db_user.password_hash = password_service.get_password_hash(new_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def change_profile_name(session: Session, user_id: int, new_name: str):
    db_user = session.get(User, user_id)

    if not db_user:
        raise UserNotFoundException

    db_user.profile_name = new_name
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
