from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    Depends,
    Query,
    Response,
    Request,
    HTTPException,
    status,
)
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from ..service import users_controller as service
from ..service import auth as auth_service
from ..data.user import UserIn, UserAlreadyExist, UserNotFound
from ..data.admin import AdminNotCreated, Admin, AdminIn, AdminOut, AdminAlreadyExist
from ..data.users_sessions import SessionNotFound

router = APIRouter()


# Todo: on Create, Update, Delete -> resend the whole list to the api user again


@router.on_event("startup")
async def create_users_db_tables():
    service.create_users_db_tables()


# @router.post("/admin/create")
async def create_admin():
    try:
        service.create_admin()
    except AdminAlreadyExist as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=(e.msg))


# @router.get("/admin")
async def get_admin():
    try:
        return service.get_admin()
    except AdminNotCreated as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(e.msg))


@router.put("/")
async def create_user(user: Annotated[UserIn, Body()]):
    try:
        service.create_user(user)
    except UserAlreadyExist as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=(e.msg))


@router.get("/user")
async def get_user(name: Annotated[str, Query()]):
    try:
        return service.get_user(name)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(e.msg))


@router.get("/")
async def get_all_users():
    return service.get_all_users()


@router.delete("/{name}")
async def delete_user(name: str):
    try:
        service.delete_user(name)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(e.msg))


# ---------- Authentication --------------
security = HTTPBasic()


def authenticate_admin(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    try:
        admin = auth_service.authenticate_admin(
            AdminIn(name=credentials.username, password=credentials.password)
        )
        return admin
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )


def get_session_id(request: Request):
    """used by the `get_authenticated_user_from_session_id()`"""
    session_id = request.cookies.get("session_id")
    if session_id is None:
        # raise HTTPException(status_code=401, detail="Invalid session id")
        raise HTTPException(status_code=401, detail="No session id provided")
    return session_id


def get_authenticated_user_from_session_id(
    session_id: Annotated[str, Depends(get_session_id)],
):
    try:
        admin = auth_service.get_admin_from_session_id(session_id)
        if admin is None:
            raise HTTPException(status_code=401, detail="Invalid session id")
        return admin
    except SessionNotFound as e:
        raise HTTPException(status_code=401, detail="Invalid session id")
    except UserNotFound as e:
        raise HTTPException(
            status_code=404, detail="No admin with the provided session id."
        )


# ------- Admin APIs ------------


@router.get("/admin")
def read_current_user(
    admin: Annotated[AdminOut, Depends(get_authenticated_user_from_session_id)],
):
    return admin


@router.get("/session")
def get_session(session_id: Annotated[str, Depends(get_session_id)]):
    return session_id


@router.post("/login")
def login(admin: Annotated[Admin, Depends(authenticate_admin)], response: Response):
    # 0. validate user credentials
    # 1. create session
    # 2. store that session in cookie
    session = auth_service.create_session(admin)
    # httpOnly prevents js from stealing or modifying the cookie (preveting XSS attack)
    response.set_cookie(key="session_id", value=session.id, httponly=True)
    return {"message": "Logged in", "session_id": session.id}


@router.post("/logout")
def logout():
    pass
