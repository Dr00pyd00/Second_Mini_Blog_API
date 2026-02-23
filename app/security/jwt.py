from enum import Enum
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError

from app.schemas.jwt import CreateAccessTokenSchema
from app.core.config import app_settings
from app.models.users import User
from app.errors_messages.jwt import ERROR_JWT_BAD_CREDENTIALS



# access token ===================================================
# data to token : user_id user_role !
def create_access_token(
        user_data: CreateAccessTokenSchema, 
        time_delta: timedelta = None, 
        )->str:
    now = datetime.now(timezone.utc)
    
    if time_delta is None:
        expiration = now + timedelta(minutes=app_settings.access_token_expire_minutes)
    else:    
        expiration = now + time_delta
    
    to_encode = {
        "sub": str(user_data.user_id),
        "exp": expiration,
        "role": user_data.user_role.value,
        "iat": now, # issued at
    }

    encoded_jwt_token = jwt.encode(
        claims=to_encode,
        key=app_settings.secret_key,
        algorithm=app_settings.algorithm,
    )     

    return encoded_jwt_token


# refresh Token ========================================================
# data to token : user_id user_role !
def create_refresh_token(
        user_data: CreateAccessTokenSchema, 
        time_delta: timedelta = None, 
        )->str:
    now = datetime.now(timezone.utc)
    
    if time_delta is None:
        expiration = now + timedelta(minutes=app_settings.refresh_token_expire_minutes)
    else:    
        expiration = now + time_delta
    
    to_encode = {
        "sub": str(user_data.user_id),
        "exp": expiration,
        "role": user_data.user_role.value,
        "iat": now, # issued at
    }

    encoded_jwt_token = jwt.encode(
        claims=to_encode,
        key=app_settings.secret_key,
        algorithm=app_settings.algorithm,
    )     

    return encoded_jwt_token


#==============================
#==== VERIFY TOKEN ============
#==============================
# verify if contain good payload and return user_id (int)
def verify_jwt(token:str)->int:
    """Return user_id (int) or raise HTTPException"""
    try:
        payload = jwt.decode(
            token=token,
            key=app_settings.secret_key,
            algorithms=[app_settings.algorithm],
        )
        user_id: str | None = payload.get("sub") 
        if user_id is None:
            raise ERROR_JWT_BAD_CREDENTIALS
        return int(user_id)
    except JWTError:
        raise ERROR_JWT_BAD_CREDENTIALS
