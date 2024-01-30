from sqlmodel import Session, select, col
from fastapi import Request, HTTPException, status
from typing import Optional
from datetime import datetime, timedelta

from ..model.access_session import AccessSession, AccessSessionRead
from ..model.exceptions import NotValidAccessSession, AccessSessionNotFound
from shared.models import User


def get_session(db: Session, session_uuid: str) -> AccessSession:
    access_session = db.exec(
        select(AccessSession).where(AccessSession.uuid == session_uuid)
    ).first()
    if not access_session:
        raise AccessSessionNotFound
    return access_session


def create_session(db: Session, user_id: int, user_agent: str):
    access_session = AccessSession(user_id=user_id, user_agent=user_agent)
    db.add(access_session)
    db.commit()
    db.refresh(access_session)
    return access_session


def delete_session(db: Session, uuid: str):
    access_session = get_session(db, uuid)
    db.delete(access_session)
    db.commit()


def get_all_online_users(db: Session):
    from dependencies import get_settings

    config = get_settings()

    online_filter = col(AccessSession.last_seen) >= datetime.utcnow() - timedelta(
        minutes=config.session_threshold
    )
    stmt = select(AccessSession).where(online_filter)
    access_sessions = db.exec(stmt).all()

    users: set[User] = set()
    for access_session in access_sessions:
        users.add(access_session.user)

    return list(users)


def update_access_session_last_seen(db: Session, uuid: str):
    access_session = get_session(db, uuid)
    access_session.last_seen = datetime.utcnow()
    db.add(access_session)
    db.commit()


def validate_access_session(
    db: Session, session_uuid: str, request: Request
) -> AccessSession:
    # validate that the session is stored in the DB
    access_session = get_session(db, session_uuid)

    # validate session user-agent (must match)
    if not request.headers.get("User-Agent") == access_session.user_agent:
        raise NotValidAccessSession(msg="User-Agent does not match.")
    return access_session
