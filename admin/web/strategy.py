from fastapi import APIRouter


router = APIRouter(tags=["Strategies Management"])

@router.post("")
async def create_strategy():
    '''create a new strategy and store it in the DB'''
    pass
@router.post("/notify")
async def notify_users_about_strategy(users_ids: list[int], strategy_id: int):
    pass

@router.delete("")
async def delete_strategy(strategy_id):
    pass

@router.get("")
async def get_all_strategies():
    pass