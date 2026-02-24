from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from app.models.users import RoleEnum, User
from app.dependencies.database import get_db
from app.schemas.users import UserCreationSchema
from app.security.password_users import hash_user_pw
from app.errors_messages.users import ERROR_USERNAME_ALREADY_TAKEN


# get user or return a 404 HTTPException
def get_user_by_id_or_404(
        id: int,
        db: Session,
)->User:
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User ID:{id} not found."
        )
    return user

# create user  ==============================================
def create_user_service(
        user_data: UserCreationSchema,
        db: Session,
)->User:
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise ERROR_USERNAME_ALREADY_TAKEN

    user_data_dict = user_data.model_dump()
    user_data_dict["password"] = hash_user_pw(user_data_dict["password"])

    new_user = User(**user_data_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

    
# Change user status (by a admin) ===========================================
def change_user_status_by_admin_service(
        user_id: int,
        new_role: RoleEnum,
        db: Session,
)->User:
    user_to_update = get_user_by_id_or_404(id=user_id, db=db)
    user_to_update.role = new_role
    db.commit()
    db.refresh(user_to_update)

    return user_to_update
