from fastapi import status, HTTPException



# post not found:
ERROR_POST_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="post not found."
)


# post already soft deleted:
ERROR_POST_SOFT_DELETED = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Post soft deleted."
)


# if user try delete other user post:
ERROR_USER_CANT_DELETE_OTHER_USER_POST = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You can't delete post you NOT owner."
)

# user try update post not owner
ERROR_USER_CANT_UPDATE_OTHER_USER_POST = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You can't update post you NOT owner."
)