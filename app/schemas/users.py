from typing import Optional
import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator

from app.models.mixins.status_mixin import StatusEnum
from app.models.users import RoleEnum


# for create new user
class UserCreationSchema(BaseModel):

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username is <str>: 3 to 50 char."
    )
    password: str = Field(
        ...,
        min_length=5,
        max_length=90,
        description="Password is <str>: 5 to 90 char."
    )

    email: Optional[EmailStr] = None

    @field_validator("username") 
    @classmethod
    def username_alphanumeric(cls, name:str)->str:
        if re.match(r'^[a-zA-Z0-9_]+$', name) is None:
            raise ValueError("<username> must be alphanumeric (can contain '_').")
        return name
    
    @field_validator("password")
    @classmethod
    def password_complexity(cls, pw:str)->str:
        if not any(char.isdigit() for char in pw):
            raise ValueError("<password> must contain at least ONE digit.")
        if not any(char.isalpha() for char in pw):
            raise ValueError("<password> must contain at least ONE alphabetic char.")
        return pw
    

# for login
class UserLoginSchema(BaseModel):
    username: str
    password: str

# user data frontend can see
class UserDataFromDbSchema(BaseModel):
    id: int
    username: str 
    status: str
    role: str
    created_at: datetime

    model_config={"from_attributes":True}

# user role when  patch for change role
class UserSwapRoleFormSchema(BaseModel):
    new_role: RoleEnum

# user status when patch for change status
class UserSwapStatusFormSchema(BaseModel):
    new_status: StatusEnum


# FILTERS ====================================================
class UsersFilterRoleStatusSchema(BaseModel):
    # if field is a unknown ( by enum)  send error
    model_config = ConfigDict(extra="forbid")

    role: RoleEnum | None = None
    status: StatusEnum | None = None
    deleted: bool = False


