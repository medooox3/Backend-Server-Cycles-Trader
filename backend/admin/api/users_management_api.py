from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status

from ..service import users_controller as service
from ..db.user import UserIn, UserAlreadyExist, UserNotFound
from ..db.admin import AdminNotCreated

router = APIRouter()



# Todo: on Create, Update, Delete -> resend the whole list to the api user again


@router.on_event("startup")
async def create_users_db_tables():
    service.create_users_db_tables()

@router.get("/admin")
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
    

@router.get("/{name}")
async def get_user(name: str):
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
    
