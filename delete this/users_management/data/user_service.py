from typing import Optional
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from security.utils import password_utils
from .user import UserCreate, User, UserSearch, UserUpdate
from .license import License, LicenseUpdate, LicenseCreate
from .account import Account, AccountCreate
from user.cycles.data.cycle import Cycle, CycleRead

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
)

AccountNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
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
    # todo: refactor to work with account 
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


# ******************** Account ********************
def create_account(session: Session, user_id: int, account: AccountCreate) -> Account:
    a = Account.model_validate(account)
    session.add(a)
    session.commit()
    session.refresh(a)
    return a


def get_account_from_uuid(session: Session, uuid: str) -> Account:
    account = session.exec(select(Account).where(Account.uuid == uuid)).first()
    if not account:
        raise AccountNotFoundException
    return account

def get_all_accounts(session: Session, user_id: Optional[int]) -> list[Account]:
    """returns all accounts stored in the DB, or all accounts of a specific user"""
    stmt = select(Account)
    if user_id:
        stmt = select(Account).where(Account.user_id == user_id)

    return list(session.exec(stmt).all())


def delete_accounts(
    session: Session, user_id: Optional[int], accounts_ids: Optional[list[int]]
):
    if accounts_ids:
        for account_id in accounts_ids:
            session.delete(session.get(Account, account_id))
    if user_id:
        for account in get_all_accounts(session, user_id):
            session.delete(account)
    session.commit()


def update_account():
    pass


# ? ******************** End Account ********************


# ******************** License ********************
def get_all_licenses(session: Session):
    return session.exec(select(License)).all()


def get_account_license(session: Session, account_id: int) -> License:
    account = session.get(Account, account_id)
    if not account:
        raise AccountNotFoundException
    license = account.license
    if not license:
        raise LicenseNotFoundException
    return license


def get_user_licenses(session: Session, user_id: int) -> list[License]:
    user = session.get(User, user_id)
    if not user:
        raise UserNotFoundException
    licenses = user.licenses
    if licenses is None:
        raise LicenseNotFoundException
    return licenses


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
    db_license = session.get(License, license_id)
    if not db_license:
        raise LicenseNotFoundException
    user = db_license.user
    if not user:
        raise UserNotFoundException
    return user


def create_account_license(
    session: Session, account_id: int, license: LicenseCreate
) -> License:
    # find account
    account = session.get(Account, account_id)
    if not account:
        raise AccountNotFoundException

    if account.license:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already has a license, consider removing the old license and creating a new one or updating the old license.",
        )
    # add license to the db
    db_license = License(
        **license.model_dump(exclude_unset=True),
        account_id=account.id,
        user_id=account.user_id,
    )
    session.add(db_license)
    session.commit()
    session.refresh(db_license)

    # link the license to the user
    db_license.user = account.user
    # link license to account
    account.license = db_license

    session.commit()
    session.refresh(db_license)
    return db_license


def delete_license(session: Session, account_id: int):
    license = get_account_license(session, account_id)
    session.delete(license)
    session.commit()


def update_license(session: Session, account_id: int, license: LicenseUpdate):
    from datetime import datetime

    db_license = get_account_license(session, account_id)

    # update license attributes
    for field, value in license.model_dump(exclude_unset=True).items():
        setattr(db_license, field, value)
    db_license.updated_at = datetime.utcnow()

    session.add(db_license)
    session.commit()
    session.refresh(db_license)
    return db_license


# ? ******************** End License ********************


# ******************** Cycles ********************
def get_user_cycles(session: Session, user_id: int) -> list[CycleRead]:
    cycles = session.exec(select(Cycle).where(Cycle.user_id == user_id)).all()
    return [CycleRead.model_validate(cycle) for cycle in cycles]


# ? ******************** End Cycles ********************
