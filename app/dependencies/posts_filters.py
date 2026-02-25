

from typing import Annotated

from fastapi import Query

from app.models.mixins.status_mixin import StatusEnum
from app.schemas.posts import PostGetAllFilters


def get_post_filters(
        status: Annotated[StatusEnum | None, Query(..., description="posts status you want to se..")] = None,
        see_deleted: Annotated[bool, Query(description="True if you want see soft deleted posts.")] = False,

)->PostGetAllFilters:

    return PostGetAllFilters(
        status=status,
        see_deleted=see_deleted,
    )
    