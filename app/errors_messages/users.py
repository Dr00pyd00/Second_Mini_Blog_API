from curses.ascii import HT

from fastapi import HTTPException, status

ERROR_USERNAME_ALREADY_TAKEN = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Username already taken."
)

ERROR_ADMIN_CANT_SELF_CHANGE_ROLE = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="An Admin can't change his own role."
)

ERROR_ADMIN_OR_MODERATOR_CANT_SELF_CHANGE_STATUS = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Admin or Moderator can't change his own status."
)

ERROR_MODERATOR_CANT_CHANGE_ADMIN_STATUS = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Moderator can't modify a Admin Status."
)

ERROR_ADMIN_CANT_SELF_DELETE_USER = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Admin can't delete his own user."
)

ERROR_USER_CANT_DELETE_OTHER_USER = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="can't delete other user account."
)

ERROR_USER_SOFT_DELETED = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="user soft deleted."
)

ERROR_CANT_DELETE_LAST_ADMIN = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Last admin can't be deleted."
)

ERROR_EMAIL_ALREADY_TAKEN = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Email already taken."
)