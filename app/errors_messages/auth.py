from curses.ascii import HT

from fastapi import HTTPException, status


# Invalid credentials when login
ERROR_INVALID_CREDENTIALS_LOGIN = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid Credentials"
)