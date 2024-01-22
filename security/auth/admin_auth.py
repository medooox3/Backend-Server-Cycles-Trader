from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer


admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token/admin")


AdminAuth = Annotated[str, Depends(admin_oauth2_scheme)]
