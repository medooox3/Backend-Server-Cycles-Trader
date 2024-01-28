from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated


from dependencies import DBSession
from security.web.auth_api import get_active_user
from shared.models import UserRead, CycleRead, CycleCreate, CycleUpdate
from ..service import trading_service


router = APIRouter()


# UserDependency = Annotated[UserRead, Depends(get_user)]
UserDependency = Annotated[UserRead, Depends(get_active_user)]

# ! Todo: when the user cycles change send new data to all connected clients
# Todo: research SSE to send notification of change to all connected clients


@router.get("/", response_model=list[CycleRead])
async def get_all_cycles(session: DBSession, user: UserDependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return trading_service.get_all_cycles(session, user.id)


# @router.post("/", response_model=CycleRead)
async def create_cycle(session: DBSession, user: UserDependency, cycle: CycleCreate):
    # ^ Cycles should be created by an order
    pass
    # cycle_db = trading_service.create_cycle(session, user.id, cycle)
    # return cycle_db


@router.patch("/")
async def update_cycle(
    session: DBSession, user: UserDependency, uuid: str, cycle: CycleUpdate
):
    cycle_db = trading_service.update_cycle(session, user.id, uuid, cycle)
    return cycle_db


@router.delete("/")
async def delete_cycle(session: DBSession, user: UserDependency, uuid: str):
    trading_service.delete_cycle(session, user.id, uuid)
