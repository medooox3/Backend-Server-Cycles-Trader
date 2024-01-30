from sqlmodel import Session
from shared.models import User, UserRead
from shared.services import accounts_service, license_service, users_service


def get_license(session: Session, account_uuid: str):
    # account = accounts_service.get_account_from_uuid(session, account_uuid)
    return license_service.get_account_license(session, account_uuid)


def change_profile_name(session: Session, user: UserRead, name: str):
    return users_service.change_profile_name(session, user.id, name)


def update_session_last_seen():
    # Todo 
    pass
