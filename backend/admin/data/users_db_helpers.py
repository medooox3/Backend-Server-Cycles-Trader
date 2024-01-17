from typing import Annotated
from sqlmodel import create_engine, Session, SQLModel, select

from .user import User, UserIn, UserOut
from .user import UserNotFound, UserAlreadyExist
from .admin import Admin, AdminOut, AdminNotCreated, AdminAlreadyExist
from .users_sessions import UserSession, SessionNotFound, UserSessionModel


engine = create_engine("sqlite:///users.db", echo=True)


def create_db_tables():
    SQLModel.metadata.create_all(engine)


# ------- Admin --------
def create_admin():
    try:
        if get_admin():
            raise AdminAlreadyExist()

    except AdminNotCreated:
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
        result = session.exec(select(User).where(User.name is username)).first()
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


# ----------- Users Sessions ------------
def create_session(admin: Admin) -> UserSessionModel:
    from uuid import uuid4

    user_session = UserSessionModel(id=str(uuid4()), user_id=admin.id)
    with Session(engine) as session:
        session.add(UserSession(id=user_session.id, user_id=user_session.user_id))
        session.commit()
    return user_session


def delete_session(user_session: str):
    with Session(engine) as session:
        session.delete(user_session)
        session.commit()


def get_session(session_id: str) -> UserSessionModel:
    with Session(engine) as session:
        user_session = session.exec(
            select(UserSession).where(UserSession.id == session_id)
        ).first()
        if user_session:
            return UserSessionModel(id=user_session.id, user_id=user_session.user_id)
        raise SessionNotFound("Session Not Found")


def get_admin_from_session(user_session: UserSessionModel) -> AdminOut:
    print(user_session.user_id)
    print(user_session.id)
    
    with Session(engine) as session:
        admin = session.exec(
            select(Admin).where(Admin.id == user_session.user_id)
        ).first()
        if admin:
            admin_out = AdminOut(id=admin.id, name=admin.name)
            return admin_out
        raise UserNotFound(msg="Can't find Admin from session")


def get_admin_from_session_id(session_id: str) -> AdminOut:
    session = get_session(session_id)
    if session:
        return get_admin_from_session(session)
    raise UserNotFound("Can't find Admin from session")


def get_all_user_sessions(user_id: str) -> list[UserSessionModel]:
    # todo: refactor
    with Session(engine) as session:
        result = session.exec(
            select(UserSession).where(UserSession.user_id == user_id)
        ).all()
        sessions = [
            UserSessionModel(id=session.id, user_id=session.user_id) for session in result
        ]
        return sessions
