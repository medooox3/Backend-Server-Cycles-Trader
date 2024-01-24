from sqlmodel import Session, select
from fastapi import HTTPException, status

from cycle import Cycle, CycleCreate, CycleUpdate, CycleRead
from users_management.data.user import User


async def create_cycle(session: Session, cycle: CycleCreate, user_id: int) -> Cycle:
    db_cycle = Cycle(**cycle.model_dump())
    session.add(db_cycle)
    session.commit()
    session.refresh(db_cycle)
    return db_cycle


async def delete_cycle(session: Session, cycle_id: int):
    session.delete(session.get(Cycle, cycle_id))
    session.commit()


async def update_cycle(session: Session, cycle_id: int, cycle: CycleUpdate) -> Cycle:
    db_cycle = session.get(Cycle, cycle_id)
    if not db_cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cycle not found"
        )
    for field, value in cycle.model_dump(exclude_unset=True).items():
        setattr(db_cycle, field, value)
    session.add(db_cycle)
    session.commit()
    session.refresh(db_cycle)
    return db_cycle


def get_all_cycles(session: Session, user_id: int) -> list[CycleRead]:
    cycles = session.exec(select(Cycle).where(Cycle.user_id == user_id)).all()
    return [CycleRead.model_validate(cycle) for cycle in cycles]


def get_cycle(session: Session, cycle_id: int) -> CycleRead:
    cycle = session.get(Cycle, cycle_id)
    if not cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cycle not found"
        )
    return CycleRead.model_validate(cycle)
