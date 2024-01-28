from fastapi import APIRouter, status, HTTPException, Query
from dependencies import DBSession
from users_management.data import user_repo, UserRead, User
from user.cycles.data.cycle import Cycle, CycleRead, CycleUpdate

router = APIRouter(prefix="/cycles")


@router.get("/", response_model=list[CycleRead])
async def get_all_cycles(session: DBSession, user_id: int):
    return user_repo.get_user_cycles(session, user_id)

async def update_cycle():
    pass
