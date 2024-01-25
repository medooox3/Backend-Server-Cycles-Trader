from typing import Optional
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from security.utils import password_utils
from .user import UserCreate, User, UserSearch, UserUpdate
from .license import License, LicenseUpdate, LicenseCreate
from user.cycles.data.cycle import Cycle, CycleRead

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
)
LicenseNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User does not have a license or license is not valid.",
)
LicenseNotValidException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="License is not valid.",
)


def _map_user(user: UserCreate) -> User:
    """Convert UserCreate to User"""
    return User(
        # Lower, so that no same user name can be created (ex: ali, Ali)
        name=user.name.lower(),
        email=user.email,
        location=user.location,
        phone=user.phone,
        password_hash=password_utils.get_password_hash(user.password),
    )


def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)


def get_user_by_name(session: Session, name: str) -> Optional[User]:
    return session.exec(select(User).where(User.name == name)).first()


def get_all_users(session: Session) -> list[User]:
    return list(session.exec(select(User)).all())


def create_user(session: Session, user: UserCreate) -> User:
    # Todo: raise exceptions if user is found in the DB or any attribute is not unique
    db_user = _map_user(user)
    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exist: name, email, phone must be unique",
        )


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
        user = find_user_of_license(session, filter.license_id)
    else:
        user = None

    if not user:
        raise UserNotFoundException

    return user


def delete_user(session: Session, filter: UserSearch):
    user = find_user_using_filter(session, filter)

    # Find and delete all related objects
    if user.license:
        session.delete(user.license)
    if user.cycles:
        for cycle in user.cycles:
            session.delete(cycle)

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


def change_profile_name(session: Session, user_id: int, new_name: str):
    db_user = session.get(User, user_id)

    if not db_user:
        raise UserNotFoundException

    db_user.profile_name = new_name
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# * ------------ License ---------------


def get_all_licenses(session: Session):
    return session.exec(select(License)).all()


def get_user_license(session: Session, user_id: int) -> License:
    user = session.get(User, user_id)
    if not user:
        raise UserNotFoundException
    license = user.license
    if not license:
        raise LicenseNotFoundException
    return license


def validate_license(license: License) -> bool:
    from datetime import datetime

    is_expired = (
        license.expire_date < datetime.utcnow()
        or license.start_date >= license.expire_date
    )
    if is_expired:
        license.valid = False
    return license.valid


def find_user_of_license(session: Session, license_id: int) -> User:
    user = session.exec(select(User).where(User.license_id == license_id)).first()
    if not user:
        raise UserNotFoundException
    return user


def create_user_license(
    session: Session, user_id: int, license: LicenseCreate
) -> License:
    # find user
    user = session.get(User, user_id)
    if not user:
        raise UserNotFoundException

    if user.license:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already has a license, consider removing old one and creating a new one or updating the old license.",
        )
    # add license to the db
    db_license = License.model_validate(license)
    session.add(db_license)
    session.commit()
    session.refresh(db_license)

    # link license to user
    user.license = db_license
    session.commit()
    session.refresh(db_license)
    return db_license


def delete_license(session: Session, user_id: int):
    license = get_user_license(session, user_id)
    session.delete(license)
    session.commit()


def update_license(session: Session, user_id: int, license: LicenseUpdate):
    from datetime import datetime

    db_license = get_user_license(session, user_id)

    # update license attributes
    for field, value in license.model_dump(exclude_unset=True).items():
        setattr(db_license, field, value)
    db_license.updated_at = datetime.utcnow()

    session.add(db_license)
    session.commit()
    session.refresh(db_license)
    return db_license


# ******************** Cycles ********************
def get_user_cycles(session: Session, user_id: int) -> list[CycleRead]:
    cycles = session.exec(select(Cycle).where(Cycle.user_id == user_id)).all()
    return [CycleRead.model_validate(cycle) for cycle in cycles]
