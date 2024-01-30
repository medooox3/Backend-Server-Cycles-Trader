from typing import Annotated

from fastapi import Depends, APIRouter, Request
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import DBSession
from shared.models import Token
from admin.features.admin_management.service import admin as admin_service
from security.service.auth import validate_user_login, validate_admin_login


router = APIRouter(tags=["Authentication"])


@router.post("", response_model=Token)
async def login_for_token(
    session: DBSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request,
) -> Token:
    form_data.username = form_data.username.lower()

    if admin_service.find_admin_by_email(session, email=form_data.username):
        token = validate_admin_login(session, form_data.username, form_data.password)
    else:
        token = validate_user_login(
            session, form_data.username, form_data.password, request
        )

    return token
