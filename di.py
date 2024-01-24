"""Dependency Injection Module"""

from sqlmodel import Session
from fastapi import Depends
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
