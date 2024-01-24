from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select


from di import DBSession
from ..model.token_model import Token, TokenData
from admin.data.admin import Admin
from admin.data import admin_repo
from ..utils import jwt_utils, password_utils


from users_management.data import user_repo
from users_management.data.user import User


router = APIRouter(tags=["Authentication"])
admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/admin")
user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/user")


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

# * --------- User Auth ---------------- *
@router.post("/user")
async def user_login_for_token(
    session: DBSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    UnAuthorizedException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
    
    user = user_repo.get_user_by_name(session, form_data.username)
    if not user:
        raise UnAuthorizedException
    if not password_utils.verify_password(form_data.password, user.password_hash):
        raise UnAuthorizedException

    #  Todo: Later i can modify the token data to accept the session number to be able to count and 
    # revoke a session from the backend
    access_token = jwt_utils.create_access_token(
        token_data=TokenData(sub=user.name, admin=False)
    )
    token = Token(access_token=access_token)
    return token
    # return {"access_token": payload, "token_type": "bearer"}

def get_user(session: DBSession, token: Annotated[str, Depends(user_oauth2_scheme)]):
    """a dependency to get the user from the DB, injecting this function
    into the router of the routes that need user authorization.   
    
    Using this returned user from the dependency all the coming operations will use his id to perform api operations.
    For example all the functions to create  a cycle will require a user id in the argument
    list and using this id will insert the data in the database and link the user to them.
    """
    
    token_data = jwt_utils.verify_token_access(token)
    user = user_repo.get_user_by_name(session, token_data.sub)
    # ^ Using this returned user all the coming operations will use his id to perform api operations ^
    # For example all the functions to create a license or a cycle will require a user id in the argument
    # list and using this id will insert the data in the database and link the user to them.
    return user

