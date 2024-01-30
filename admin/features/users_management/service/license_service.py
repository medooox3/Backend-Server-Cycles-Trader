from datetime import datetime
from sqlmodel import Session, select
from ..data import (
    User,
    License,
    LicenseUpdate,
    LicenseCreate,
    Account,
)
from ..data.exceptions import (
    UserNotFoundException,
    AccountNotFoundException,
    LicenseNotFoundException,
    LicenseAlreadyExists,
    LicenseNotValidException,
)


def get_all_licenses(session: Session):
    return session.exec(select(License)).all()


def get_account_license(session: Session, account_uuid: str) -> License:
    account = session.exec(select(Account).where(Account.uuid == account_uuid)).first()
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




def get_user_of_license(session: Session, license_id: int) -> User:
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
        raise LicenseAlreadyExists
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


def delete_license(session: Session, account_uuid: str):
    license = get_account_license(session, account_uuid)
    session.delete(license)
    session.commit()


def update_license(session: Session, account_uuid: str, license: LicenseUpdate):
    from datetime import datetime

    db_license = get_account_license(session, account_uuid)

    # update license attributes
    for field, value in license.model_dump(exclude_unset=True).items():
        setattr(db_license, field, value)
    db_license.updated_at = datetime.utcnow()

    session.add(db_license)
    session.commit()
    session.refresh(db_license)
    return db_license


# ? ******************** End License ********************
