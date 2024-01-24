from fastapi import HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from security.utils import password_utils
from .admin import AdminCreate, Admin, AdminUpdate


def get_admin(session: Session):
    return session.get(Admin, "admin")


def get_admin_using_email(session: Session, email: str):
    try:
        admin = session.exec(select(Admin).where(Admin.email == email.lower())).one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found. couldn't find email"
        )
    except MultipleResultsFound:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fatal Error Multiple admins found, please contact support",
        )
    return admin


def create_admin(session: Session, admin: AdminCreate):
    if get_admin(session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Admin already exists"
        )
    db_admin = Admin(
        email=admin.email.lower(),
        password_hash=password_utils.get_password_hash(admin.password),
    )
    session.add(db_admin)
    session.commit()
    session.refresh(db_admin)
    return db_admin


def update_admin(session: Session, admin: AdminUpdate):
    db_admin = session.exec(select(Admin).where(Admin.name == "Admin")).first()
    if not db_admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found."
        )
    for field, value in admin.model_dump(exclude_unset=True).items():
        if field == "password":
            field = "password_hash"
            value = password_utils.get_password_hash(value)
        setattr(db_admin, field, value)
    session.add(db_admin)
    session.commit()
    session.refresh(db_admin)
    return db_admin
