from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated


from di import DBSession
from security.web.auth_api import get_user
from users_management.data.user import User, UserRead
from ..data import cycles_repo
from ..data.cycle import Cycle, CycleRead, CycleCreate, CycleUpdate, CycleReadWithUser

router = APIRouter()


UserDependency = Annotated[UserRead, Depends(get_user)]


@router.get("/", response_model=list[CycleRead])
async def get_all_cycles(session: DBSession, user: UserDependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return cycles_repo.get_all_cycles(session, user.id)  


@router.post("/", response_model=CycleRead)
async def create_cycle(session: DBSession, user: UserDependency, cycle: CycleCreate):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    cycle_db = cycles_repo.create_cycle(session, user.id, cycle)
    return cycle_db
