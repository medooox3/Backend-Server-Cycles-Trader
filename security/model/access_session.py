import shortuuid

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from shared.models import User


class AccessSession(SQLModel, table=True):
    __tablename__: str = "access_session"

    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(index=True, default_factory=lambda: shortuuid.uuid())
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # if user is last seen during (threshold 'last 5 minutes') consider him online
    last_seen: datetime = Field(default_factory=datetime.utcnow)
    user_agent: Optional[str] = Field(
        default=None,
        description="Identify the client (web app or local software), local software must provide a predetermined user-agent to allow certain access",
    )
    # Todo: May be add the ip of the client (for more security)

    user_id: int = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="access_sessions")


class AccessSessionRead(SQLModel):
    id: int
    uuid: str
    user_id: int
    user_agent: Optional[str]
    created_at: datetime
    last_seen: datetime
    is_online: bool


# class AccessSessionSearch(SQLModel):
#     id: Optional[int] = None
#     uuid: Optional[str] = None
#     user_id: Optional[int] = None
#     user_agent: Optional[str] = None # Metatrader clinet, React-client
#     is_online: Optional[bool] = None
