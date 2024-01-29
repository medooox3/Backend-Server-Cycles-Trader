from fastapi import APIRouter


router = APIRouter()


@router.post("/")
async def send():
    pass


@router.get("/")
async def listen():
    pass
