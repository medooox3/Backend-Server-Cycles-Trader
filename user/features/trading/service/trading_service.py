'''All Trading occurs on the metatrader platform, so any call to the api, must
create an event that calls the meta-trader platform and when the platform receives
the order and run it, it will send the new data to the backend to update all the web
clients
'''

from sqlmodel import Session, select
from fastapi import HTTPException, status

from shared.models import (
    User,
    Cycle,
    CycleCreate,
    CycleUpdate,
    CycleRead,
    Order,
)


def create_cycle(session: Session, account_uuid: str, cycle: CycleCreate) -> Cycle:
    '''create a cycle and link it to an account'''
    # before creating any cycle for this user , check the number of previous cycles and
    # add one to them
    # user = session.get(User, user_id)
    # cycle_number = 0
    # if user and user.cycles is not None:
    #     cycle_number = len(user.cycles) + 1
    db_cycle = Cycle(**cycle.model_dump(), account_uuid=account_uuid)
    # db_cycle.number = cycle_number
    session.add(db_cycle)
    session.commit()
    session.refresh(db_cycle)
    return db_cycle


def create_order(session: Session, order: Order):
    # todo: send this order to the Local client
    # and when the local client receives it, he will create a new cycle
    # and sends this cycle to the backend to store.
    pass


def delete_cycle(session: Session, account_uuid: str, uuid: str):
    '''remove a cycle from an account'''
    # todo: verify that this cycle belongs to this user before deleting or updating

    cycle = session.exec(select(Cycle).where(Cycle.uuid == uuid)).first()
    if not cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cycle not found"
        )
    if not cycle.account_uuid == account_uuid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    session.delete(cycle)
    session.commit()


def update_cycle(
    session: Session, account_uuid: str, uuid: str, cycle: CycleUpdate
) -> Cycle:
    db_cycle = session.exec(select(Cycle).where(Cycle.uuid == uuid)).first()
    if not db_cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cycle not found"
        )
    if not db_cycle.account_uuid == account_uuid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    for field, value in cycle.model_dump(exclude_unset=True).items():
        setattr(db_cycle, field, value)
    session.add(db_cycle)
    session.commit()
    session.refresh(db_cycle)
    return db_cycle


def get_all_cycles(session: Session, account_uuid: str) -> list[CycleRead]:
    cycles = session.exec(select(Cycle).where(Cycle.account_uuid == account_uuid)).all()
    return [CycleRead.model_validate(cycle) for cycle in cycles]


def get_cycle(session: Session, uuid: str) -> CycleRead:
    cycle = session.exec(select(Cycle).where(Cycle.uuid == uuid)).first()
    if not cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cycle not found"
        )
    return CycleRead.model_validate(cycle)
