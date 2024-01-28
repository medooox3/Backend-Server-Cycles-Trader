from fastapi import APIRouter, status
from dependencies import DBSession
from ..data import Account, AccountCreate
from ..service import accounts_service


router = APIRouter()


@router.post("/", response_model=Account)
async def create_account(
    session: DBSession, user_id: int, account: AccountCreate
) -> Account:
    a = accounts_service.create_account(session, user_id, account)
    return a


@router.get("/", response_model=list[Account])
async def get_user_accounts(session: DBSession, user_id: int):
    return accounts_service.get_all_accounts(session, user_id)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(session: DBSession, user_id: int, account_id: int):
    accounts_service.delete_accounts(session, user_id, accounts_ids=[account_id])


async def update_account():
    pass
