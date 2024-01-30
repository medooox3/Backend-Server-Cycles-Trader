from fastapi import APIRouter, status
from dependencies import DBSession
from ..service import users_service, license_service
from ..data.license import License, LicenseUpdate, LicenseCreate

router = APIRouter()


@router.post("/", response_model=License)
async def create_new_license(
    session: DBSession, account_uuid: str, license: LicenseCreate
) -> License:
    return license_service.create_account_license(session, account_uuid, license)


# @router.get("/{user_id}", response_model=License)
# async def get_license_by_user_id(session: DBSession, user_id: int):
#     return user_repo.get_user_license(session, user_id)


@router.get("/", response_model=list[License])
async def get_all_licenses(session: DBSession):
    return license_service.get_all_licenses(session)


@router.patch("/", response_model=License)
async def update_license(*, session: DBSession, account_uuid: str, license: LicenseUpdate):
    return license_service.update_license(session, account_uuid, license)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_license(session: DBSession, account_uuid: str):
    license_service.delete_license(session, account_uuid)
