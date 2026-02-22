from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.models.users import User
from app.dependencies.database import get_db
from app.security.jwt import verify_jwt
from app.services.users import get_user_by_id_or_404


# find the username/password in the header automic
oauth2_scheme =OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[Session, Depends(get_db)],
)->User:
    
    user_id = verify_jwt(token=token)
    user = get_user_by_id_or_404(id=user_id, db=db) 
    return user