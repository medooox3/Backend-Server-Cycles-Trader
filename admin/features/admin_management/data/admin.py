from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from typing import Optional


class AdminBase(SQLModel):
    email: EmailStr = Field(unique=True)
    profile_name: Optional[str] = Field(default="admin")


class Admin(AdminBase, table=True):
    name: str = Field(default="admin", primary_key=True)
    password_hash: str = Field(..., alias="password")


class AdminCreate(AdminBase):
    password: str = Field(min_length=8)


class AdminRead(AdminBase):
    name: str


class AdminUpdate(SQLModel):
    email: Optional[str] = None
    password: Optional[str] = None
    profile_name: Optional[str] = None
