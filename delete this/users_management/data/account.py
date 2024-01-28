from sqlmodel import SQLModel, Relationship, Field
import shortuuid
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User, UserRead
    from .license import License, LicenseRead
    from user.cycles.data.cycle import Cycle


class AccountBase(SQLModel):
    name: Optional[str] = Field(index=True)
    uuid: str = Field(index=True, default_factory=lambda: str(shortuuid.uuid()))
    metatrader_id: str = Field(index=True)


class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    # ********** Relationships *************
    user: Optional["User"] = Relationship(back_populates="accounts")
    license: Optional["License"] = Relationship(back_populates="account")
    cycles: Optional[list["Cycle"]] = Relationship(back_populates="account")


# class AccountRead(AccountBase):
#     user: UserRead
#     license: Optional["LicenseRead"]


class AccountCreate(AccountBase):
    user_id: int
