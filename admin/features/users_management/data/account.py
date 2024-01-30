from sqlmodel import SQLModel, Relationship, Field
import shortuuid
from uuid import uuid4
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User, UserRead, License
    from .license import LicenseRead
    from shared.models import Cycle, CycleRead


class AccountBase(SQLModel):
    name: Optional[str] = Field(index=True)
    metatrader_id: str = Field(..., unique=True, index=True)


class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: uuid4().hex, index=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    # ********** Relationships *************
    user: Optional["User"] = Relationship(back_populates="accounts")
    license: Optional["License"] = Relationship(back_populates="account")
    cycles: Optional[list["Cycle"]] = Relationship(back_populates="account")


class AccountRead(AccountBase):
    # user_id: int
    # user: "UserRead"
    uuid: str
    license: "LicenseRead"
    cycles: list["CycleRead"]


class AccountCreate(AccountBase):
    # user_id: int
    pass
