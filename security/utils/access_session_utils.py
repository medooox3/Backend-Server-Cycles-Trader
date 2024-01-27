from sqlmodel import Session, select, col
from fastapi import Request, HTTPException, status
from typing import Optional
from datetime import datetime, timedelta

from ..model.access_session import AccessSession, AccessSessionRead


NotValidAccessSession = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Please Login."
)


def validate_access_session(
    db: Session, access_session_uuid: str, request: Request
) -> AccessSession:
    access_session = db.exec(
        select(AccessSession).where(AccessSession.uuid == access_session_uuid)
    ).first()

    if not access_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Session not found. Please Login.",
        )

    if not request.headers.get("User-Agent") == access_session.user_agent:
        # raise NotValidAccessSession
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User-Agent does not match. Please Login.",
        )

    return access_session


def create_access_session(
    db: Session, user_id: int, user_agent: str
) -> AccessSessionRead:
    access_session = AccessSession(user_id=user_id, user_agent=user_agent)
    db.add(access_session)
    db.commit()
    db.refresh(access_session)
    return map_to_access_session_read(db, [access_session])[0]


def update_access_session(db: Session, access_session: AccessSession) -> None:
    access_session.last_seen = datetime.utcnow()
    db.add(access_session)
    db.commit()


def delete_access_session(db: Session, access_session: AccessSession) -> None:
    db.delete(access_session)
    db.commit()


def get_online_status(db: Session, session_id: int) -> bool:
    THRESHOLD = timedelta(minutes=5)

    access_session = db.get(AccessSession, session_id)
    if not access_session:
        raise NotValidAccessSession

    if datetime.utcnow() - access_session.last_seen >= THRESHOLD:
        return False
    else:
        return True


def get_all_access_sessions(
    db: Session,
    is_online: Optional[bool] = None,
    user_agent: Optional[str] = None,
) -> list[AccessSessionRead]:
    online_filter = col(AccessSession.last_seen) >= datetime.utcnow() - timedelta(
        minutes=5
    )
    user_agent_filter = col(AccessSession.user_agent == user_agent)

    stmt = select(AccessSession)
    if is_online:
        stmt = stmt.where(online_filter)
    if user_agent:
        stmt = stmt.where(user_agent_filter)

    db_sessions = list(db.exec(stmt).all())
    return map_to_access_session_read(db, db_sessions)


def get_access_sessions_of_user(db: Session, user_id: int) -> list[AccessSessionRead]:
    db_access_sessions = db.exec(
        select(AccessSession).where(AccessSession.user_id == user_id)
    ).all()
    return map_to_access_session_read(db, list(db_access_sessions))


def update_access_session_last_seen(db: Session, session_uuid: str):
    access_session = db.exec(
        select(AccessSession).where(AccessSession.uuid == session_uuid)
    ).first()
    if not access_session:
        raise NotValidAccessSession
    access_session.last_seen = datetime.utcnow()
    db.add(access_session)
    db.commit()
    db.refresh(access_session)
    return access_session


def map_to_access_session_read(
    db: Session, access_sessions: list[AccessSession]
) -> list[AccessSessionRead]:
    """Conver access session to access session read which contains online status"""
    return [
        AccessSessionRead(
            **db_session.model_dump(),
            is_online=get_online_status(db, db_session.id),  # type: ignore
        )
        for db_session in access_sessions
    ]
