from pydantic import BaseModel

from app.models.users import RoleEnum

# needed for create token user_id + user_role

class CreateAccessTokenSchema(BaseModel):
    user_id: int
    user_role: RoleEnum = RoleEnum.USER
