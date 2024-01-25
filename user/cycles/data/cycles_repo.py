from sqlmodel import Session, select
from fastapi import HTTPException, status

from .cycle import Cycle, CycleCreate, CycleUpdate, CycleRead
from users_management.data.user import User


def create_cycle(session: Session, user_id: int, cycle: CycleCreate) -> Cycle:
    # before creating any cycle for this user , check the number of previous cycles and
    # add one to them
    # user = session.get(User, user_id)
    # cycle_number = 0
    # if user and user.cycles is not None:
    #     cycle_number = len(user.cycles) + 1
    db_cycle = Cycle(**cycle.model_dump(), user_id=user_id)
    # db_cycle.number = cycle_number
    session.add(db_cycle)
    session.commit()
    session.refresh(db_cycle)
    return db_cycle


def delete_cycle(session: Session, user_id: int, uuid: str):
    # todo: verify that this cycle belongs to this user before deleting or updating

    cycle = session.exec(select(Cycle).where(Cycle.uuid == uuid)).first()
    if not cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cycle not found"
        )
    if not cycle.user_id == user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    session.delete(cycle)
    session.commit()


def update_cycle(
    session: Session, user_id: int, uuid: str, cycle: CycleUpdate
) -> Cycle:
    db_cycle = session.exec(select(Cycle).where(Cycle.uuid == uuid)).first()
    if not db_cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cycle not found"
        )
    if not db_cycle.user_id == user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    for field, value in cycle.model_dump(exclude_unset=True).items():
        setattr(db_cycle, field, value)
    session.add(db_cycle)
    session.commit()
    session.refresh(db_cycle)
    return db_cycle


def get_all_cycles(session: Session, user_id: int) -> list[CycleRead]:
    cycles = session.exec(select(Cycle).where(Cycle.user_id == user_id)).all()
    return [CycleRead.model_validate(cycle) for cycle in cycles]


def get_cycle(session: Session, uuid: str) -> CycleRead:
    cycle = session.exec(select(Cycle).where(Cycle.uuid == uuid)).first()
    if not cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cycle not found"
        )
    return CycleRead.model_validate(cycle)
