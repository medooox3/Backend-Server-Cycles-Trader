from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated


from di import DBSession
from ..data import admin_repo
from ..data.admin import Admin, AdminRead, AdminCreate, AdminUpdate
from security.web import auth_api

# --------------
# from security.auth import admin_auth
# --------------

router = APIRouter(tags=["Admin"])


@router.post("/", response_model=AdminRead)
async def register_admin(session: DBSession, admin: AdminCreate):
    return admin_repo.create_admin(session, admin)


# ! This is a security issue, using oauth sceheme will allow any authorized user/ admin to access this
@router.get("/", response_model=AdminRead, dependencies=[Depends(auth_api.get_admin)])
async def get_admin(session: DBSession):
    admin = admin_repo.get_admin(session)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found, Please register first.",
        )
    return admin


@router.patch("/", response_model=AdminRead, dependencies=[Depends(auth_api.get_admin)])
async def update_admin(session: DBSession, admin: AdminUpdate):
    return admin_repo.update_admin(session, admin)
