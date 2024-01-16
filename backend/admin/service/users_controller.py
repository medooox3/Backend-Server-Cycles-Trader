from ..db import users_db_helpers as data
from ..db.user import UserIn


def create_user(user: UserIn):
    data.create_user(user)


def delete_user(username: str):
    data.delete_user(username)


def get_user(username: str):
    return data.get_user(username)


def get_all_users():
    return data.get_all_users()


def get_admin():
    return data.get_admin()
