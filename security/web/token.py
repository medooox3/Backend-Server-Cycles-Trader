from typing import Annotated
from fastapi import Depends, APIRouter, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..model import Token
from dependencies import DBSession


router = APIRouter(tags=["Authentication"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@router.post("", response_model=Token)
async def login_for_token(
    session: DBSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request,
) -> Token:
    form_data.username = form_data.username.lower()
    # todo : validate if this is an admin or not
    # if admin_repo.get_admin_using_email(session, form_data.username):
    # if the DB already has a user with these credentials log him in
    if (
        session.exec(select(User).where(User.name == form_data.username)).first()
        is not None
    ):
        token = validate_user(session, form_data.username, form_data.password, request)
    else:
        token = validate_admin(session, form_data.username, form_data.password)

    return token
