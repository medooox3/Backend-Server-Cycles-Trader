from sqlmodel import SQLModel, Relationship, Field
from typing import Optional, TYPE_CHECKING
from uuid import uuid4
from datetime import datetime


if TYPE_CHECKING:
    from shared.models import Cycle
    from security.model.access_session import AccessSession
    from users_management.data.account import Account
    from .license import License


class UserBase(SQLModel):
    name: str = Field(index=True, unique=True)
    profile_name: Optional[str] = Field(default="user")
    email: Optional[str] = Field(index=True, unique=True, default=None)
    phone: Optional[str] = Field(index=True, unique=True, default=None)
    location: Optional[str] = Field(default=None)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), index=True)
    # trade_id: str # if needed
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: Optional[datetime] = Field(default=None, index=True)
    

    # ********* Relationships *********
    licenses: Optional[list["License"]] = Relationship(back_populates="user")
    accounts: Optional[list["Account"]] = Relationship(back_populates="user")
    access_sessions: list["AccessSession"] = Relationship(back_populates="user")


class UserRead(UserBase):
    id: int
    uuid: str


class UserCreate(UserBase):
    # todo: this needs to be hashed and verified
    password: str


class UserUpdate(SQLModel):
    name: Optional[str] = None
    profile_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    password: Optional[str] = None


class UserSearch(SQLModel):
    """Used to find user using any of these attributes"""

    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    uuid: Optional[str] = None
    license_id: Optional[int] = None


# class UserReadWithLicense(UserRead):
#     license: Optional["License"] = Field(default=None)


# class UserReadAll(UserReadWithCycles, UserReadWithLicense):
#     pass
