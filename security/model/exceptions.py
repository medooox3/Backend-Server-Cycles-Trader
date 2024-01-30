from fastapi import HTTPException, status


# ************** Sessions *************
class NotValidAccessSession(HTTPException):
    def __init__(self, msg: str | None = None, detail="Please Login."):
        if msg:
            detail = f"{detail} - {msg}"

        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


AccessSessionNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Access Session not found.",
)


# ************** Authentication *************

UserNotFoundException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User not found.",
)

WrongCredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Wrong Credentials",
)

# ************** Authorization *************
UnAuthorizedAccessException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Un Authroized Access. Please Login.",
)


# ************** Token *************
TokenCredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Couldn't verify Token credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
