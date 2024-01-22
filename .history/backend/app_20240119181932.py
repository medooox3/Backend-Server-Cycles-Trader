from fastapi import FastAPI
from admin.api.users_management_api import router as users_management_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
app.include_router(users_management_router, prefix="/users", tags=["Users"])



