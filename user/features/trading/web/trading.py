from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated


from dependencies import DBSession
from security.dependencies import get_user
from shared.models import UserRead, CycleRead, CycleCreate, CycleUpdate, Order
from ..service import trading_service


router = APIRouter()


# UserDependency = Annotated[UserRead, Depends(get_user)]
UserDependency = Annotated[UserRead, Depends(get_user)]

# ! Todo: when the user cycles change send new data to all connected clients
# Todo: research SSE to send notification of change to all connected clients

# ^ Todo: each client (local / web ) will sent what identifies it,
# ^ Then by creating a dependency it will identify the client upon request.


@router.get("/", response_model=list[CycleRead])
async def get_all_cycles(session: DBSession, account_uuid: str, user: UserDependency):
    # todo: need account to get the cycles related to that account
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return trading_service.get_all_cycles(session, account_uuid)


@router.post("/", response_model=CycleRead)
async def create_cycle(session: DBSession, user: UserDependency, account_uuid: str, cycle: CycleCreate):
    # Todo: the local client is the one responsible for creating a cycle
    # ^ Cycles should be created by an order
    cycle_db = trading_service.create_cycle(session, account_uuid, cycle)
    return cycle_db
    # cycle_db = trading_service.create_cycle(session, user.id, cycle)
    # return cycle_db


@router.post("/order")
async def craete_order(user: UserDependency, order: Order):
    """The web app is responsible for creating an order, when the order is created
    using this endpoint an event will be sent to the local client to create the order
    and when the order is created, the local client will create the new cycle.
    The caller of this function will await for it to send either a success or failure.
    if the order event is sent to the local client and the local client acknowledged that it received the order then this function will return a success other wise it will wait for a minute, while the message broker retries and if it fails it will return a failure.
    """


@router.patch("/")
async def update_cycle(
    session: DBSession,
    user: UserDependency,
    cycle_uuid: str,
    account_uuid: str,
    cycle: CycleUpdate,
):
    """can be called by both the local client and the web client, calling this end point from local client will only trigger a change in the db, but if called from the web app then an event will be sent to the local client to process the new data and update the cycle."""
    cycle_db = trading_service.update_cycle(session, account_uuid, cycle_uuid, cycle)
    return cycle_db


@router.delete("/")
async def delete_cycle(
    session: DBSession, user: UserDependency, cycle_uuid: str, account_uuid: str
):
    trading_service.delete_cycle(session, account_uuid, cycle_uuid)
