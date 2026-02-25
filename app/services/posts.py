



from typing import List
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.errors_messages.users import ERROR_USER_CANT_DELETE_OTHER_USER
from app.models.posts import Post
from app.errors_messages.posts import (
    ERROR_POST_NOT_FOUND,
    ERROR_POST_SOFT_DELETED,
    ERROR_USER_CANT_DELETE_OTHER_USER_POST
)
from app.models.users import User
from app.schemas.posts import PostCreationForm, PostGetAllFilters

# get post or 404

def get_post_or_404(post_id: int, db: Session)->Post:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise ERROR_POST_NOT_FOUND
    return post


# ================================================
# ============= CRUD =============================
# ================================================

############ GET #################################

# all posts + pagination + filters 
def get_all_posts_service(
        #current_user: User,
        post_filter: PostGetAllFilters,
        db: Session,
        skip: int, 
        limit: int,
)->List[User]:

    query = db.query(Post)

    # filters:
    if post_filter.status:
        query = query.filter(User.status == post_filter.status)
    if not post_filter.see_deleted:
        query = query.filter(Post.deleted_at == None)
    
    # pagination:
    query = (query
             .order_by(Post.created_at)
             .offset(skip)
             .limit(limit)
             
    )

    posts = query.all()
    return posts


######### POST #################################

# create post:
def create_post_service(
        current_user: User,
        new_post_data: PostCreationForm,
        db: Session,
)-> Post:
    
    new_post = Post(
        **new_post_data.model_dump(),
        user_id=current_user.id,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


############# DELETE ################################

# delete a post by ID:
def soft_delete_post_by_id_service(
        current_user: User,
        post_id: int, 
        db: Session
)->Post:
    post = get_post_or_404(post_id=post_id, db=db) 

    # check if post not already deleted:
    if post.deleted_at is not None:
        raise ERROR_POST_SOFT_DELETED
    
    # check is current_user is owner:
    if current_user.id != post.user_id:
        raise ERROR_USER_CANT_DELETE_OTHER_USER_POST
    
    post.deleted_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(post)

    return post
