from fastapi import HTTPException, status

ERROR_USERNAME_ALREADY_TAKEN = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Username already taken."
)

ERROR_ADMIN_CANT_SELF_CHANGE_ROLE = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="An Admin can't change his own role."
)