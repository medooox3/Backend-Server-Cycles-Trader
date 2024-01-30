from fastapi import HTTPException, status


AdminNotFountException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found."
)

MultipleAdminAccountsFoundException = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Fatal Error Multiple admins found, please contact support",
)

AdminAlreadyExistsException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Admin already exists, can't create again!",
)

AdminNotCreatedException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Admin not created, Please register first.",
)
