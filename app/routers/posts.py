from typing import Annotated, List

from fastapi import APIRouter, Depends, Query, status, Body, Path
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.dependencies.jwt import get_current_user
from app.dependencies.posts_filters import get_post_filters
from app.schemas.posts import PostCreationForm, PostDataFromDbSchema, PostGetAllFilters, PostPatchFormSchema 
from app.models.users import User
from app.services.posts import create_post_service, get_all_posts_service, get_post_by_id_service, soft_delete_post_by_id_service, update_patch_post_service
from app.dependencies.database import get_db



router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


#############################################
###### PUBLIC ###############################
#############################################


# ============== GET =================================== #

# get all posts:
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[PostDataFromDbSchema])
def get_all_posts(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    post_filters: Annotated[PostGetAllFilters, Depends(get_post_filters)],
    skip: Annotated[int, Query(ge=0, description="number of posts to skip in db.")] = 0,
    limit: Annotated[int, Query(ge=0, le=100, description="number of posts send in request: 1 to 100 max.")] =  10,

)->List[PostDataFromDbSchema]:
    return get_all_posts_service(
        post_filter=post_filters,
        db=db,
        skip=skip,
        limit=limit,
    )


# get one post by ID:
@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostDataFromDbSchema)
def get_post_by_id(
    current_user: Annotated[User, Depends(get_current_user)],
    post_id: Annotated[int, Path(..., description="ID of the post you want to get.")],
    db: Annotated[Session, Depends(get_db)],
)->PostDataFromDbSchema:
    return get_post_by_id_service(
        post_id=post_id,
        db=db,
    )
# ============== POST =================================== #

# create new post:
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostDataFromDbSchema)
def create_new_post(
    current_user: Annotated[User, Depends(get_current_user)],
    new_post_data: Annotated[PostCreationForm, Body(..., description="datas inputs for new post creation.")],
    db: Annotated[Session, Depends(get_db)],
)->PostDataFromDbSchema:
    return create_post_service(
        current_user=current_user,
        new_post_data=new_post_data,
        db=db,
    )
# ============== PUT =================================== #
# ============== PATCH =================================== #

# update patch post 
@router.patch("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostDataFromDbSchema)
def update_patch_post(
    current_user: Annotated[User, Depends(get_current_user)],
    post_id: Annotated[int, Path(..., description="post ID you want to soft delete.")],
    db: Annotated[Session, Depends(get_db)],
    post_data: Annotated[PostPatchFormSchema, Body(description="fields for posts data update.")] = None,
)->PostDataFromDbSchema:
    return update_patch_post_service(
        current_user=current_user,
        post_data=post_data,
        post_id=post_id,
        db=db,
    )
# ============== DELETE =================================== #

# delete post by ID:
@router.delete("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostDataFromDbSchema)
def soft_delete_post_by_id(
    current_user: Annotated[User, Depends(get_current_user)],
    post_id: Annotated[int, Path(..., description="post ID you want to soft delete.")],
    db: Annotated[Session, Depends(get_db)],
)->PostDataFromDbSchema:
    return soft_delete_post_by_id_service(
        current_user=current_user,
        post_id=post_id,
        db=db
    )


#############################################
###### ADMIN  ###############################
#############################################


# ============== GET =================================== #
# ============== POST =================================== #
# ============== PUT =================================== #
# ============== PATCH =================================== #
# ============== DELETE =================================== #