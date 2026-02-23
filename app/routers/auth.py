from typing import Annotated

from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.jwt import BearerTokenAfterLoginSchema
from app.dependencies.database import get_db
from app.models.users import User
from app.services.auth import login_service


# login : send username + passwor = return acces_token bearer


router = APIRouter(
    tags=["Authentication"]
)


# Login ============================================
@router.post("/login", status_code=status.HTTP_200_OK, response_model=BearerTokenAfterLoginSchema)
def login(
    user_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
)->BearerTokenAfterLoginSchema:
   
   return login_service(user_form=user_form, db=db)
