from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select, Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound


from di import DBSession
from ..model.token_model import Token, TokenData
from admin.data.admin import Admin
from admin.data import admin_repo
from ..utils import jwt_utils, password_utils


from users_management.data import user_repo
from users_management.data.user import User, UserRead, UserReadWithLicense
from users_management.data.license import License, LicenseUpdate


router = APIRouter(tags=["Authentication"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
# admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/admin")
# user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/user")


UnAuthorizedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect Credentials",
)


@router.post("", response_model=Token)
async def login_for_token(
    session: DBSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    form_data.username = form_data.username.lower()
    # todo : validate if this is an admin or not
    # if admin_repo.get_admin_using_email(session, form_data.username):
    # if the DB already has a user with these credentials log him in
    if (
        session.exec(select(User).where(User.name == form_data.username)).first()
        is not None
    ):
        token = validate_user(session, form_data.username, form_data.password)
    else:
        token = validate_admin(session, form_data.username, form_data.password)

    return token


def get_user(
    session: DBSession, token: Annotated[str, Depends(oauth2_scheme)]
) -> UserRead:
    token_data = jwt_utils.verify_token_access(token)
    if token_data.admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = user_repo.get_user_by_name(session, token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return UserRead.model_validate(user)


def get_active_user(session: DBSession, user: Annotated[UserRead, Depends(get_user)]):
    """returns active user according to his license status"""
    try:
        license = user_repo.get_user_license(session, user.id)
        if license:
            return user
        else: 
            raise user_repo.LicenseNotFoundException
    except:
        raise


def get_admin(session: DBSession, token: Annotated[str, Depends(oauth2_scheme)]):
    token_data = jwt_utils.verify_token_access(token)
    if not token_data.admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin not found",
        )
    admin = admin_repo.get_admin(session)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin not found, err 1012"
        )
    return admin


def validate_user(session: Session, username: str, password: str):
    user = user_repo.get_user_by_name(session, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found. couldn't find username",
        )
    if not password_utils.verify_password(password, user.password_hash):
        raise UnAuthorizedException

    access_token = jwt_utils.create_access_token(
        token_data=TokenData(sub=user.name, admin=False)
    )
    token = Token(access_token=access_token)
    return token


def validate_admin(session: Session, username: str, password: str):
    # admin = session.get(Admin, username)
    admin = admin_repo.get_admin_using_email(session, username)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin not found. couldn't find username",
        )
        # raise UnAuthorizedException
    if not password_utils.verify_password(password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin wrong password",
        )

    access_token = jwt_utils.create_access_token(
        token_data=TokenData(sub=admin.name, admin=True)
    )
    token = Token(access_token=access_token)
    return token


#     #  Todo: Later i can modify the token data to accept the session number to be able to count and
#     # revoke a session from the backend
