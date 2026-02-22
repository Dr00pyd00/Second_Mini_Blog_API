from fastapi import HTTPException, status

ERROR_USERNAME_ALREADY_TAKEN = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Username already taken."
)