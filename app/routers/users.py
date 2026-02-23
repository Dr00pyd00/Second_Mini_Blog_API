from typing import Annotated, List

from fastapi import APIRouter, status, Depends, Body
from sqlalchemy.orm import Session

from app.schemas.users import UserCreationSchema, UserDataFromDbSchema
from app.models.users import RoleEnum, User
from app.dependencies.database import get_db
from app.services.users import create_user_service
from app.dependencies.jwt import get_current_user, get_user_by_id_or_404
from app.dependencies.jwt import required_roles

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


# /me 
@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserDataFromDbSchema)
def get_me(
        current_user_role_required: Annotated[User, Depends(required_roles(RoleEnum.USER))] 
)->UserDataFromDbSchema:
    
    return current_user_role_required


# List of all users for admin only:
@router.get("/all_list", status_code=status.HTTP_200_OK, response_model=List[UserDataFromDbSchema])
def get_all_users(
    admin_user: Annotated[User, Depends(required_roles(RoleEnum.ADMIN))],
    db: Annotated[Session, Depends(get_db)],
)->List[UserDataFromDbSchema]:
    users = db.query(User).all()

    return users