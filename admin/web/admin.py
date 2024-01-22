from fastapi import APIRouter
from ..data import admin_repo
from ..data.admin import Admin, AdminRead, AdminCreate, AdminUpdate
from di import DBSession


# --------------
# from security.auth import admin_auth
# --------------

router = APIRouter(tags=["Admin"])


@router.post("/", response_model=AdminRead)
async def register_admin(session: DBSession, admin: AdminCreate):
    return admin_repo.create_admin(session, admin)


@router.get("/", response_model=AdminRead)
async def get_admin(session: DBSession):
    return admin_repo.get_admin(session)


@router.patch("/", response_model=AdminRead)
async def update_admin(session: DBSession, admin: AdminUpdate):
    return admin_repo.update_admin(session, admin)


