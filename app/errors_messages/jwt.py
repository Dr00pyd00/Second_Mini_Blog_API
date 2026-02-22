from fastapi import HTTPException, status



ERROR_JWT_BAD_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid JWT Credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)