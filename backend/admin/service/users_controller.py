from ..data import users_db_helpers as data
from ..data.user import UserIn



# ----------- Admin -------------

def create_admin():
    data.create_admin()

# ----------- Users -------------

def create_users_db_tables():
    data.create_db_tables()


def create_user(user: UserIn):
    user = UserIn(name=user.name.lower(), password=user.password)
    data.create_user(user)


def delete_user(username: str):
    data.delete_user(username)


def get_user(username: str):
    username = username.lower()
    return data.get_user(username)


def get_all_users():
    return data.get_all_users()


def get_admin():
    return data.get_admin()
