from fastapi import HTTPException, status
from sqlmodel import Session
from .admin import AdminCreate, Admin, AdminUpdate
from security.utils import password_utils


def get_admin(session: Session):
    return session.get(Admin, "Admin")


def create_admin(session: Session, admin: AdminCreate):
    if get_admin(session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Admin already exists"
        )
    db_admin = Admin(
        email=admin.email,
        password_hash=password_utils.get_password_hash(admin.password),
    )
    session.add(db_admin)
    session.commit()
    session.refresh(db_admin)
    return db_admin


def update_admin(session: Session, admin: AdminUpdate):
    db_admin = get_admin(session)
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
