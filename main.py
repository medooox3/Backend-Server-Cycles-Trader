from fastapi import FastAPI
from  admin.web.admin import router as admin_router 


app = FastAPI()
app.include_router(admin_router, prefix="/admin", tags=["Admin"])


@app.get("/")
async def root():
    return {"message": "Hello World"}