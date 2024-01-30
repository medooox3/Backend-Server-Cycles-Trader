from sqlmodel import Session, select
from shared.models import Cycle, CycleRead


def get_user_cycles(session: Session, user_id: int) -> list[CycleRead]:
    cycles = session.exec(select(Cycle).where(Cycle.user_id == user_id)).all()
    return [CycleRead.model_validate(cycle) for cycle in cycles]
