from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from uuid import uuid4
if TYPE_CHECKING:
    from users_management.data.user import User, UserRead
    from users_management.data.account import Account
# Todo: I Think i should remove the number () and only identify the cycle by id (not shown) 

class CycleBase(SQLModel):
    # generated using the logic: (len(user_cycles) + 1)
    symbol: str
    tp: int
    sl: int
    tf: str
    lot: float
    count: int
    candle: str
    auto: bool


class Cycle(CycleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), index=True)
    # number: int
    
    account_id: Optional[int] = Field(default=None, foreign_key="account.id")
    account: Optional["Account"] = Relationship(back_populates="cycles")


class CycleCreate(CycleBase):
    pass


class CycleRead(CycleBase):
    id: int
    uuid: str
    # number: int
    


class CycleReadWithUser(CycleRead):
    user: Optional["UserRead"] = Field(default=None)


class CycleUpdate(SQLModel):
    symbol: str | None = None
    tp: int | None = None
    sl: int | None = None
    tf: str | None = None
    lot: float | None = None
    count: int | None = None
    candle: str | None = None
    auto: bool | None = None
