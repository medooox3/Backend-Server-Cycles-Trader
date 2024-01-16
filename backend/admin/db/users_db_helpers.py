from typing import Annotated
from .user import User, UserIn, UserOut
from .user import UserNotFound, UserAlreadyExist
from .admin import Admin, AdminNotCreated, AdminAlreadyExist
from sqlmodel import create_engine, Session, SQLModel, select


engine = create_engine("sqlite:///users.db", echo=True)


def create_db_tables():
    SQLModel.metadata.create_all(engine)


# ------- Admin --------
def create_admin():
    admin = get_admin()
    if admin:
        raise AdminAlreadyExist()
    with Session(engine) as session:
        from uuid import uuid4

        admin_ = Admin(id=str(uuid4()), name="admin", password_hash="admin")
        session.add(admin_)
        session.commit()


def get_admin():
    with Session(engine) as session:
        result = session.exec(select(Admin)).first()
        if result:
            return result
        raise AdminNotCreated()


# ------- Users --------
def get_user(username: str) -> UserOut | None:
    with Session(engine) as session:
        result = session.exec(select(User).where(User.name == username)).first()
        if result:
            user = UserOut(id=result.id, name=result.name)
            return user
        raise UserNotFound()


def get_all_users() -> list[UserOut]:
    with Session(engine) as session:
        result = session.exec(select(User)).all()
        users = [UserOut(id=user.id, name=user.name) for user in result]
        return users


def create_user(user_in: UserIn):
    # if user is in the DB -> raise the error
    try:
        user = get_user(user_in.name)
        if user:
            raise UserAlreadyExist()
    # If there is not user in the DB -> create one
    except UserNotFound:
        from uuid import uuid4

        with Session(engine) as session:
            user = User(
                id=str(uuid4()), name=user_in.name, password_hash=user_in.password
            )
            session.add(user)
            session.commit()


def delete_user(username: str):
    user_out = get_user(username)
    if user_out:
        with Session(engine) as session:
            user = session.get(User, user_out.id)
            session.delete(user)
            session.commit()
