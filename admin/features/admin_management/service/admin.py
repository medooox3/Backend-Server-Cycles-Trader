from sqlmodel import Session, select
from security.service import password_service
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from ..data import (
    Admin,
    AdminUpdate,
    AdminCreate,
    AdminAlreadyExistsException,
    AdminNotFountException,
    MultipleAdminAccountsFoundException,
    AdminNotCreatedException
)


def get_admin(session: Session) -> Admin:
    admin = session.get(Admin, "admin")
    if not admin:
        raise AdminNotCreatedException
    return admin


def get_admin_using_email(session: Session, email: str) -> Admin:
    try:
        admin = session.exec(select(Admin).where(Admin.email == email.lower())).one()
    except NoResultFound:
        raise AdminNotFountException
    except MultipleResultsFound:
        raise MultipleAdminAccountsFoundException
    return admin


def find_admin_by_email(session: Session, email:str):
    return session.exec(select(Admin).where(Admin.email == email.lower())).first()

def create_admin(session: Session, admin: AdminCreate):
    if session.exec(select(Admin)).first():
        raise AdminAlreadyExistsException
    db_admin = Admin(
        email=admin.email.lower(),
        password=password_service.get_password_hash(admin.password),
    )
    session.add(db_admin)
    session.commit()
    session.refresh(db_admin)
    return db_admin


def update_admin(session: Session, admin: AdminUpdate):
    db_admin = get_admin(session)
    for field, value in admin.model_dump(exclude_unset=True).items():
        if field == "password":
            value = password_service.get_password_hash(value)
        setattr(db_admin, field, value)
    session.add(db_admin)
    session.commit()
    session.refresh(db_admin)
    return db_admin
