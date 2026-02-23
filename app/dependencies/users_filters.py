




from typing import Annotated

from fastapi import Query

from app.models.mixins.status_mixin import StatusEnum
from app.models.users import RoleEnum
from app.schemas.users import UsersFilterRoleStatusSchema


def get_user_filter_role_status(
        role: Annotated[RoleEnum | None, Query(description="Filter by role.")] = None,
        status: Annotated[StatusEnum | None, Query(description="Filter by status.")] = None,
        deleted: Annotated[bool, Query(description="filter if deleted.")] = False,
)-> UsersFilterRoleStatusSchema:
    return UsersFilterRoleStatusSchema(
        role=role,
        status=status,
        deleted=deleted
    )