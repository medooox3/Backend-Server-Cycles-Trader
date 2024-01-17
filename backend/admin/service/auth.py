from ..data.admin import AdminIn, Admin, AdminOut
from ..service import users_controller as users_service
from ..data import users_db_helpers as db_helper
from ..data.users_sessions import UserSession, UserSessionModel


# ------------- Functions ---------------
def hash_password(password):
    # todo: hash password and return the hashed result
    return password


def authenticate_admin(admin_creds: AdminIn):
    admin: Admin = users_service.get_admin()
    if not (
        admin.name == admin_creds.name
        and admin.password_hash == hash_password(admin_creds.password)
    ):
        raise Exception("Incorrect username or password")
    return admin


# Session Management
def create_session(admin: Admin):
    return db_helper.create_session(admin)


def delete_session(user_session: str):
    db_helper.delete_session(user_session)


def get_session(session_id: str)-> UserSessionModel:
    return db_helper.get_session(session_id)


def get_admin_from_session(user_session: UserSessionModel)-> AdminOut:
    return db_helper.get_admin_from_session(user_session)


def get_admin_from_session_id(session_id: str):
    session = get_session(session_id)
    if session:
        return get_admin_from_session(session)


def get_all_admin_sessions(session_id: str)-> list[UserSessionModel]:
    admin = get_admin_from_session_id(session_id)
    if admin:
        return db_helper.get_all_user_sessions(admin.id)
    return []
