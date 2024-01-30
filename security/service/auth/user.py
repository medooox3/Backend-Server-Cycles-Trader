from typing import Annotated
from fastapi import Depends, HTTPException, status, Request
from sqlmodel import Session

from security.model import Token, TokenData
from shared.models import UserRead, User
from security.model.exceptions import (
    WrongCredentialsException,
    UserNotFoundException,
    UnAuthorizedAccessException,
)
from security.service import jwt_service, password_service, access_session_service
from admin.features.users_management.service import (
    users_service,
    license_service,
    accounts_service,
)
from dependencies import DBSession

from .auth import oauth2_scheme


def validate_user_login(
    session: Session, username: str, password: str, request: Request
):
    """
    validate user credentials and creates an access session and a token.

    The request is used to validate the session user-agent"""

    user = users_service.get_user_by_name(session, username)
    if not user:
        raise UserNotFoundException
    if not password_service.verify_password(password, user.password_hash):
        raise WrongCredentialsException

    user_agent = request.headers.get("User-Agent")
    if not user_agent:
        raise UnAuthorizedAccessException

    user = UserRead.model_validate(user)
    access_session = access_session_service.create_session(session, user.id, user_agent)

    access_token = jwt_service.create_access_token(
        token_data=TokenData(
            sub=user.name,
            session=access_session.uuid,
        )
    )
    token = Token(access_token=access_token)
    return token


def get_user(
    session: DBSession,
    token: Annotated[str, Depends(oauth2_scheme)],
    request: Request,
) -> UserRead:
    token_data = jwt_service.verify_token_access(token)
    # ^ May be this check if removed will allow the admin to access all the user path operations ??
    if token_data.sub == "admin":
        raise UnAuthorizedAccessException
    user = users_service.get_user_by_name(session, token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    # Todo: validate the user session
    if not token_data.session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session not found. Please Login.",
        )
    access_session = access_session_service.validate_access_session(
        session, token_data.session, request
    )  # type: ignore

    return UserRead.model_validate(user)  # , access_session


def get_user_session():
    """Returns access session with associated UserRead"""
    pass


def get_account(session: DBSession, account_uuid: str):
    return accounts_service.validate_account_license(session, account_uuid)
