from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select


from di import DBSession
from ..model.token_model import Token, TokenData
from admin.data.admin import Admin
from admin.data import admin_repo
from ..utils import jwt_utils, password_utils


router = APIRouter(tags=["Authentication"])
admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/admin")


@router.post("/admin")
async def admin_login_for_token(
    session: DBSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    UnAuthorizedException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
    )
    try:
        admin = admin_repo.get_admin_using_email(session, form_data.username)
    except Exception:
        raise
    if not password_utils.verify_password(form_data.password, admin.password_hash):
        raise UnAuthorizedException

    access_token = jwt_utils.create_access_token(
        token_data=TokenData(sub=admin.name, admin=True)
    )
    token = Token(access_token=access_token)
    return token
    # return {"access_token": payload, "token_type": "bearer"}


def get_admin(session: DBSession, token: Annotated[str, Depends(admin_oauth2_scheme)]):
    """a dependency to get the admin from the DB, injecting this function
    into the router of the routes that need admin access only"""
    
    token_data = jwt_utils.verify_token_access(token)
    admin = admin_repo.get_admin_using_email(session, token_data.sub)
    # ? Do i need to return the admin ?
    return admin
