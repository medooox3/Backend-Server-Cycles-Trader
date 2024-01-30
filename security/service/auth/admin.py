from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from dependencies import DBSession
from security.model import Token, TokenData
from security.service import jwt_service, password_service
from admin.features.admin_management.service import admin as admin_service

from .auth import oauth2_scheme
from security.model.exceptions import TokenCredentialsException


def get_admin(session: DBSession, token: Annotated[str, Depends(oauth2_scheme)]):
    token_data = jwt_service.verify_token_access(token)
    if not token_data.sub == "admin":
        raise TokenCredentialsException
    admin = admin_service.get_admin(session)
    return admin


def validate_admin_login(session: Session, email: str, password: str):
    """Validate the credentials and creates a token for the admin"""
    admin = admin_service.get_admin_using_email(session, email)
    if not password_service.verify_password(password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong Password",
        )

    access_token = jwt_service.create_access_token(token_data=TokenData(sub="admin"))
    token = Token(access_token=access_token)
    return token
