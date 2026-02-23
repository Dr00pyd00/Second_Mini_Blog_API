from pydantic import BaseModel

from app.models.users import RoleEnum

# needed for create token user_id + user_role


# data to send to generate a token ==================================
class CreateAccessTokenSchema(BaseModel):
    user_id: int
    user_role: RoleEnum = RoleEnum.USER


# data recieved for bearer token =====================================
class BearerTokenAfterLoginSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
