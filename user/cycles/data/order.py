from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from uuid import uuid4
import shortuuid
from enum import Enum

if TYPE_CHECKING:
    from users_management.data.user import User, UserRead


class CandleType(Enum):
    open = "open"
    close = "close"
    low = "low"
    high = "high"


class OrderCommand(Enum):
    buy = "buy"
    sell = "sell"
    buy_and_sell = "buy-sell"
    close_all = "close-all"


class OrderParameters(SQLModel):
    lot: float
    drawdown: float
    sl: float
    tp: float
    candle_type: CandleType


# TODO: Must check if the local client (running meta-trader) is online before sending
# any orders or the order will fail
class Order(SQLModel):
    command: OrderCommand
    parameters: OrderParameters


