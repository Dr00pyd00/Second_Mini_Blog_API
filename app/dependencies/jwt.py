from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.errors_messages.users import ERROR_USER_SOFT_DELETED
from app.models.users import RoleEnum, User
from app.dependencies.database import get_db
from app.security.jwt import verify_jwt
from app.services.users import get_user_by_id_or_404
from app.errors_messages.jwt import ERROR_ROLE_REQUIRED



# find the username/password in the header automic
oauth2_scheme =OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[Session, Depends(get_db)],
)->User:
    
    user_id = verify_jwt(token=token)
    user = get_user_by_id_or_404(id=user_id, db=db) 
    if user.deleted_at is not None:
        raise ERROR_USER_SOFT_DELETED
    return user


# closure for Depends and get user if role else return unauthorized 

def required_roles(*required_role:RoleEnum):
    def check_current_user_role(current_user: Annotated[User, Depends(get_current_user)]):
        if current_user.role not in required_role:
            raise ERROR_ROLE_REQUIRED
        return current_user
    return check_current_user_role