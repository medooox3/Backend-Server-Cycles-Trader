from fastapi import APIRouter, Depends, status, HTTPException
from di import DBSession
from users_management.data.account import Account, AccountCreate
from users_management.data import user_repo


router = APIRouter()


@router.post("/", response_model=Account)
async def create_account(
    session: DBSession, user_id: int, account: AccountCreate
) -> Account:
    a = user_repo.create_account(session, user_id, account)
    return a


@router.get("/", response_model=list[Account])
async def get_user_accounts(session: DBSession, user_id: int):
    return user_repo.get_all_accounts(session, user_id)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(session: DBSession, user_id: int, account_id: int):
    user_repo.delete_accounts(session, user_id, accounts_ids=[account_id])

async def update_account():
    pass