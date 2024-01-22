from fastapi import APIRouter, HTTPException, status, Depends

from di import DBSession
from ..data import admin_repo
from ..data.admin import Admin, AdminRead, AdminCreate, AdminUpdate
from security.web.auth_api import admin_oauth2_scheme

# --------------
# from security.auth import admin_auth
# --------------

router = APIRouter(tags=["Admin"])


@router.post("/", response_model=AdminRead)
async def register_admin(session: DBSession, admin: AdminCreate):
    return admin_repo.create_admin(session, admin)


@router.get("/", response_model=AdminRead, dependencies=[Depends(admin_oauth2_scheme),])
async def get_admin(session: DBSession):
    admin = admin_repo.get_admin(session)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found, Please register first.",
        )
    return admin


@router.patch("/", response_model=AdminRead, dependencies=[Depends(admin_oauth2_scheme),])
async def update_admin(session: DBSession, admin: AdminUpdate):
    return admin_repo.update_admin(session, admin)
