from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select, Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound


from dependencies import DBSession
from ..model import Token, TokenData, AccessSessionRead
from admin.features.admin_management.data import Admin
from admin.features.admin_management.service import admin as admin_service
from ..utils import jwt_utils, password_utils, access_session_utils


from admin.features.users_management.service import users_service, accounts_service, license_service
from shared.models import User, UserRead, License, LicenseUpdate


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


def get_user(
    session: DBSession,
    token: Annotated[str, Depends(oauth2_scheme)],
    request: Request,
) -> UserRead:
    token_data = jwt_utils.verify_token_access(token)
    if token_data.admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
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
    access_session = access_session_utils.validate_access_session(
        session, token_data.session, request
    )  # type: ignore

    return UserRead.model_validate(user)  # , access_session


# def get_active_user(session: DBSession, user: Annotated[UserRead, Depends(get_user)]):
#     """returns active user according to his license status"""
#     try:
#         license = user_repo.get_user_license(session, user.id)
#         if license:
#             is_valid = user_repo.validate_license(license)
#             if is_valid:
#                 return user
#             raise user_repo.LicenseNotValidException
#         else:
#             raise user_repo.LicenseNotFoundException
#     except:
#         raise


def get_active_user(
    session: DBSession, request: Request, user: Annotated[UserRead, Depends(get_user)]
):
    """returns active user according to his license status"""
    try:
        account_uuid = request.cookies.get("account")
        if not account_uuid:
            raise license_service.LicenseNotFoundException
        account = accounts_service.get_account_from_uuid(session, account_uuid)
        license = users_service.get_account_license(session, account.id)  # type: ignore
        if license:
            is_valid = license_service.validate_license(license)
            if is_valid:
                return license
            raise license_service.LicenseNotValidException
        else:
            raise license_service.LicenseNotFoundException
    except:
        raise


# def get_active_user_and_session(
#     session: DBSession, user: Annotated[UserRead, Depends(get_active_user)]
# ):
#     access_session = access_session_utils.get_access_sessions_of_user(session, user.id)[
#         0
#     ]
#     return (user, access_session)


def get_admin(session: DBSession, token: Annotated[str, Depends(oauth2_scheme)]):
    token_data = jwt_utils.verify_token_access(token)
    if not token_data.admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin not found",
        )
    admin = admin_service.get_admin(session)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin not found, err 1012"
        )
    return admin


def validate_user(session: Session, username: str, password: str, request: Request):
    user = users_service.get_user_by_name(session, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found. couldn't find username",
        )
    if not password_utils.verify_password(password, user.password_hash):
        raise UnAuthorizedException

    # todo: use request to provide user agent
    user_agent = request.headers.get("User-Agent")
    if not user_agent or not user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Agent not found. Please Login.",
        )

    access_session = access_session_utils.create_access_session(
        session, user.id, user_agent
    )  # type: ignore

    access_token = jwt_utils.create_access_token(
        token_data=TokenData(
            sub=user.name,
            session=access_session.uuid,
            admin=False,
        )
    )
    token = Token(access_token=access_token)
    return token


def validate_admin(session: Session, username: str, password: str):
    # admin = session.get(Admin, username)
    admin = admin_service.get_admin_using_email(session, username)
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
        token_data=TokenData(sub=admin.name, session="", admin=True)
    )
    token = Token(access_token=access_token)
    return token


#     #  Todo: Later i can modify the token data to accept the session number to be able to count and
#     # revoke a session from the backend
