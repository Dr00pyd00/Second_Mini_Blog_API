from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from app.models.users import User
from app.dependencies.database import get_db
from app.schemas.users import UserCreationSchema
from app.security.password_users import hash_user_pw, verify_user_pw


# get user or return a 404 HTTPException
def get_user_by_id_or_404(
        id: int,
        db: Annotated[Session, Depends(get_db)],
)->User:
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User ID:{id} not found."
        )

# create user 
def create_user_service(
        user_data: UserCreationSchema,
        db: Session,
)-> None:
    user_data_dict = user_data.model_dump()
    user_data_dict["password"] = hash_user_pw(user_data_dict["password"])

    new_user = User(**user_data_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    

