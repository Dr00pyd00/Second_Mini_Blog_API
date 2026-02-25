from typing import Annotated, List

from fastapi import APIRouter, Query, status, Depends, Body, Path
from sqlalchemy.orm import Session

from app.dependencies.users_filters import get_user_filter_role_status
from app.schemas.users import UserCreationSchema, UserDataFromDbSchema, UserSwapStatusFormSchema, UsersFilterRoleStatusSchema, UserSwapRoleFormSchema
from app.models.users import RoleEnum, User
from app.dependencies.database import get_db
from app.services.users import create_user_service, soft_delete_user_service
from app.dependencies.jwt import get_current_user, required_roles
from app.services.users import change_user_role_by_admin_service, change_user_status_by_admin_or_moderator_service

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

#######################################
########    USER    #################
#######################################

# ========== GET ====================================== #  

# /me 
@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserDataFromDbSchema)
def get_me(
        current_user: Annotated[User, Depends(get_current_user)] 
)->UserDataFromDbSchema:
    
    return current_user


# ========== POST ====================================== #  

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



# ========== PUT ====================================== #  

# ========== PATCH ====================================== #  

# ========== DELETE ====================================== # 

# delete user 
@router.delete("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserDataFromDbSchema)
def soft_delete_user(
    current_user: Annotated[User, Depends(get_current_user)],
    user_id: Annotated[int, Path(..., description="ID of the user you want to softdelete.")],
    db: Annotated[Session, Depends(get_db)],
)->UserDataFromDbSchema:
    
    return soft_delete_user_service(
        current_user=current_user,
        user_id=user_id,
        db=db,
    )


#######################################
########    ADMIN MODERATOR    ########
#######################################

# ========== GET ====================================== #  

# List of all users for admin only:
# Pagination skip/limit:
@router.get("/all_list", status_code=status.HTTP_200_OK, response_model=List[UserDataFromDbSchema])
def get_all_users(
    admin_user: Annotated[User, Depends(required_roles(RoleEnum.ADMIN))],
    db: Annotated[Session, Depends(get_db)],
    filters: Annotated[UsersFilterRoleStatusSchema, Depends(get_user_filter_role_status)],
    skip: Annotated[int, Query(ge=0, description="number of users to skip.")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="number of users in a request: 1 to 100 max.")] = 10,
)->List[UserDataFromDbSchema]:

    query = db.query(User)

    if filters.status :
        query = query.filter(User.status == filters.status)
    if filters.role :
        query = query.filter(User.role == filters.role)
    if not filters.deleted :
        query = query.filter(User.deleted_at == None )
    
    # pagination:
    query = (
        query.order_by(User.created_at)
        .limit(limit)
        .offset(skip)
    )

    return query.all()


# ========== POST ====================================== #  

# ========== PUT ====================================== #  

# ========== PATCH ====================================== #  

# change user Role as Admin only 
@router.patch("/{user_id}/role", status_code=status.HTTP_200_OK, response_model=UserDataFromDbSchema)
def change_user_role_by_admin(
    admin_user: Annotated[User, Depends(required_roles(RoleEnum.ADMIN))],
    user_id: Annotated[int, Path(..., description="user ID you want change role.")],
    new_role: Annotated[UserSwapRoleFormSchema, Body(..., description="new role to give to the user.")],
    db: Annotated[Session, Depends(get_db)],
)->UserDataFromDbSchema:
    
    return change_user_role_by_admin_service(
        admin_id=admin_user.id,
        user_id=user_id,
        new_role=new_role.new_role,
        db=db,
    )


# changer user status as Admin or Moderator only ================================
@router.patch("/{user_id}/status", status_code=status.HTTP_200_OK, response_model=UserDataFromDbSchema)
def change_user_status_by_admin_or_moderator(
    current_user: Annotated[User, Depends(required_roles(RoleEnum.ADMIN, RoleEnum.MODERATOR))],
    user_id: Annotated[int, Path(..., description="User ID you want to change status.")],
    new_status: Annotated[UserSwapStatusFormSchema, Body(..., description="new status to give to the user.")],
    db: Annotated[Session, Depends(get_db)],
):
    return change_user_status_by_admin_or_moderator_service(
        current_user=current_user,
        user_id=user_id,
        new_status=new_status.new_status,
        db=db,
    )


# ========== DELETE ====================================== # 
