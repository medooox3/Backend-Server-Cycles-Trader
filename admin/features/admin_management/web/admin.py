from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated

from dependencies import DBSession
from ..service import admin as service
from ..data import AdminRead, AdminCreate, AdminUpdate, Admin
from security.web import login
from security.dependencies import get_admin, get_user

# --------------
# from security.auth import admin_auth
# --------------

router = APIRouter()


@router.post("/", response_model=AdminRead)
async def register_admin(session: DBSession, admin: AdminCreate):
    return service.create_admin(session, admin)


# ! This is a security issue, using oauth sceheme will allow any authorized user/ admin to access this
@router.get("/", response_model=AdminRead, dependencies=[Depends(get_admin)])
async def get_admin_info(session: DBSession):
    return service.get_admin(session)


@router.patch("/", response_model=AdminRead, dependencies=[Depends(get_admin)])
async def update_admin(session: DBSession, admin: AdminUpdate):
    return service.update_admin(session, admin)
