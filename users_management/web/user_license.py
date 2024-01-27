from fastapi import APIRouter, status
from di import DBSession, AccountUuid
from users_management.data import user_repo
from users_management.data.license import License, LicenseUpdate, LicenseCreate

router = APIRouter(prefix="/licenses")


@router.post("/", response_model=License)
async def create_new_license(
    session: DBSession, account_uuid: AccountUuid, user_id: int, license: LicenseCreate
) -> License:
    return user_repo.create_account_license(session, account_id, license)
    return user_repo.create_user_license(session, user_id, license)


@router.get("/{user_id}", response_model=License)
async def get_license_by_user_id(session: DBSession, user_id: int):
    return user_repo.get_user_license(session, user_id)


@router.get("/", response_model=list[License])
async def get_all_licenses(session: DBSession):
    return user_repo.get_all_licenses(session)


@router.patch("/", response_model=License)
async def update_license(*, session: DBSession, user_id: int, license: LicenseUpdate):
    return user_repo.update_license(session, user_id, license)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_license(session: DBSession, user_id: int):
    user_repo.delete_license(session, user_id)
