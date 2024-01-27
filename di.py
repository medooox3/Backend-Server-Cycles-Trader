"""Dependency Injection Module"""

from sqlmodel import Session
from fastapi import Depends, HTTPException, Request, status
from typing import Annotated
from functools import lru_cache

from database import engine
from config import Settings


def get_session():
    with Session(engine) as session:
        yield session


# Type aliases
DBSession = Annotated[Session, Depends(get_session)]


# --------------------------------------------------


@lru_cache()
def get_settings():
    return Settings()


# Type alias
settings: Annotated[Settings, Depends(get_settings)]
# --------------------------------------------------


def get_account_uuid(request: Request) -> str:
    account_uuid = request.cookies.get("account")
    if not account_uuid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account not found. Please Login.",
        )
    return account_uuid


AccountUuid : Annotated[str, Depends(get_account_uuid)]