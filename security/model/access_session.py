import shortuuid
from datetime import datetime, timedelta
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from pydantic import computed_field


if TYPE_CHECKING:
    from shared.models import User


class AccessSession(SQLModel, table=True):
    __tablename__: str = "access_session"

    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(index=True, default_factory=lambda: shortuuid.uuid())
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_seen: datetime = Field(default_factory=datetime.utcnow)
    user_agent: Optional[str] = Field(
        default=None,
        description="Identify the client (web app or local software), local software must provide a predetermined user-agent to allow certain access",
    )
    # Todo: May be add the ip of the client (for more security)
    # ip: str
    user_id: int = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="access_sessions")


class AccessSessionRead(SQLModel):
    uuid: str
    user_id: int
    created_at: datetime
    last_seen: datetime
    user_agent: Optional[str]
    user: "User"

    @computed_field
    @property
    def is_online(self) -> bool:
        return self.last_seen > datetime.utcnow() - timedelta(minutes=5)


# class AccessSessionSearch(SQLModel):
#     id: Optional[int] = None
#     uuid: Optional[str] = None
#     user_id: Optional[int] = None
#     user_agent: Optional[str] = None # Metatrader clinet, React-client
#     is_online: Optional[bool] = None
