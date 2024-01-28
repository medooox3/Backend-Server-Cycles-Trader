from fastapi import HTTPException, status

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
)

UserAlreadyExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exist: name, email, phone must be unique",
)

AccountNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
)

LicenseAlreadyExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Account already has a license, consider removing the old license and creating a new one or updating the old license.",
)

LicenseNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User does not have a license.",
    # detail="User does not have a license or license is not valid.",
)
LicenseNotValidException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="License is not valid.",
)
