from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.models.mixins.status_mixin import StatusEnum
from app.schemas.users import UserDataFromDbSchema


# see the data:
class PostDataFromDbSchema(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    deleted_at: datetime | None
    status: StatusEnum = "ACTIVE"
    owner: UserDataFromDbSchema

# create a post:
class PostCreationForm(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=80,
        description="title of the post: 3 to 80 chars."
    )

    content: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="content text of post: 3 to 2000 chars."
    )

    published: bool = True


# Filters status:
class PostGetAllFilters(BaseModel):
    
     # if field is a unknown ( by enum)  send error
    model_config = ConfigDict(extra="forbid")

    status: StatusEnum | None = None 
    see_deleted: bool = False


# For patch :
# all possibly none and user can choice what to change
class PostPatchFormSchema(BaseModel):
    title: str | None = None
    content: str | None = None 
    published: bool = True
