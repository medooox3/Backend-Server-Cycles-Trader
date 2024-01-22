from fastapi import FastAPI
from admin.api.users_management_api import router as users_management_router

app = FastAPI()

app.include_router(users_management_router, prefix="/users", tags=["Users"])



