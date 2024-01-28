from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
import shortuuid
if TYPE_CHECKING:
    from shared.models import User, UserRead, Account

class CycleBase(SQLModel):
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
    uuid: str = Field(default_factory=lambda: shortuuid.uuid(), index=True)
    
    account_id: Optional[int] = Field(default=None, foreign_key="account.id")
    account: Optional["Account"] = Relationship(back_populates="cycles")


class CycleCreate(CycleBase):
    pass


class CycleRead(CycleBase):
    id: int
    uuid: str
    


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
