from sqlmodel import SQLModel, Relationship, Field
from uuid import uuid4
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class LicenseBase(SQLModel):
    start_date: datetime = Field(default_factory=datetime.utcnow)
    expire_date: datetime = Field(default_factory=datetime.utcnow)
    valid: bool = Field(default=False, nullable=False)


class LicenseCreate(LicenseBase):
    pass


class License(LicenseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id", unique=True)
    user: Optional["User"] = Relationship(back_populates="license")


class LicenseUpdate(SQLModel):
    key: str = str(uuid4())
    start_date: Optional[datetime] = None
    expire_date: Optional[datetime] = None
    valid: bool


class LicenseRead(LicenseBase):
    pass