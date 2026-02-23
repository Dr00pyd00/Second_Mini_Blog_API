from sqlalchemy.orm import Session

from app.schemas.users import UserLoginSchema
from app.schemas.jwt import BearerTokenAfterLoginSchema, CreateAccessTokenSchema
from app.models.users import RoleEnum, User
from app.errors_messages.auth import ERROR_INVALID_CREDENTIALS_LOGIN
from app.security.password_users import verify_user_pw
from app.security.jwt import create_access_token



def login_service(
        user_form: UserLoginSchema,
        db: Session
)->BearerTokenAfterLoginSchema:
 
    user = db.query(User).filter(User.username == user_form.username).first()
    if not user:
        raise ERROR_INVALID_CREDENTIALS_LOGIN
    # check password:
    if not verify_user_pw(user_form.password, user.password):
        raise ERROR_INVALID_CREDENTIALS_LOGIN
    
    # token creation:
    data_for_token = CreateAccessTokenSchema(
        user_id=user.id,
        user_role=user.role
    )
    token = create_access_token(user_data=data_for_token)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
    

