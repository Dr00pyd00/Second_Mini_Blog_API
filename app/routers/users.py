from typing import Annotated

from fastapi import APIRouter, status, Depends, Body
from sqlalchemy.orm import Session

from app.schemas.users import UserCreationSchema, UserDataFromDbSchema
from app.dependencies.database import get_db
from app.services.users import create_user_service

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# user creation
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserDataFromDbSchema,
)
def create_user(
    user_fields: Annotated[UserCreationSchema, Body(..., description="Fields for create new user.")],
    db: Annotated[Session, Depends(get_db)],
)->UserDataFromDbSchema:
    return create_user_service(user_data=user_fields, db=db)