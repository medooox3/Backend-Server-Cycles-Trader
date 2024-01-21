from sqlmodel import SQLModel, Relationship, Field
from uuid import uuid4, UUID
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class License(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    # ^ if expire date is None, license is valid forever
    start_date: Optional[datetime] = Field(default=None)
    expire_date: Optional[datetime] = Field(default=None)
    valid: bool = Field(default=False, nullable=False)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="license")
