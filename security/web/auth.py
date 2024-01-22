from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/token")

async def admin_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # user =  get_user(form_data.username)
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password") 
    # hashed_password = password_utils.get_password_hash(form_data.password)
    # if not password_utils.verify_password(hashed_password, user.password_hash):
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    # return {"access_token": form_data.username, "token_type": "bearer"}
    pass

async def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    pass