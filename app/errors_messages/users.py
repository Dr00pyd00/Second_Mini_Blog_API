from fastapi import HTTPException, status

ERROR_USERNAME_ALREADY_TAKEN = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Username already taken."
)

ERROR_ADMIN_CANT_SELF_CHANGE_ROLE = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="An Admin can't change his own role."
)

ERROR_ADMIN_OR_MODERATOR_CANT_SELF_CHANGE_STATUS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Admin or Moderator can't change his own status."
)