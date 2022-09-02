"""Classes related to user endpoints
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any, ClassVar, Optional

from pydantic.fields import Field

from metabase_tools.models.generic_model import Item


class User(Item):
    """User object class with related methods"""

    BASE_EP: ClassVar[str] = "/user"

    name: str = Field(alias="common_name")
    email: str
    first_name: str
    last_name: str
    date_joined: datetime
    last_login: Optional[datetime]
    updated_at: Optional[datetime]
    is_qbnewb: bool
    is_superuser: bool
    ldap_auth: Optional[bool]
    google_auth: Optional[bool]
    is_active: Optional[bool]
    locale: Optional[str]
    group_ids: Optional[list[int]]
    login_attributes: Optional[list[dict[str, Any]]]
    personal_collection_id: Optional[int]

    # @classmethod
    # def current(cls: type[GWA], adapter: MetabaseApi) -> GWA:
    #     """Current user details

    #     Args:
    #         adapter (MetabaseApi): Connection to Metabase API

    #     Raises:
    #         RequestFailure: Invalid response from API

    #     Returns:
    #         User: Current user details
    #     """
    #     response = adapter.get(endpoint="/user/current")
    #     if isinstance(response, dict):
    #         return cls(**response)
    #     raise RequestFailure

    # @classmethod
    # def disable(cls, adapter: MetabaseApi, targets: list[int]) -> dict[int, Any]:
    #     """Disables user(s) provided

    #     Args:
    #         adapter (MetabaseApi): Connection to Metabase API
    #         targets (list[int]): List of users to disable

    #     Returns:
    #         dict: Dict of users that were disabled with results
    #     """
    #     return super(User, cls).delete(adapter=adapter, targets=targets)

    # @classmethod
    # def enable(cls: type[GWA], adapter: MetabaseApi, targets: list[int]) -> list[GWA]:
    #     """Enable user(s) provided

    #     Args:
    #         adapter (MetabaseApi): Connection to Metabase API
    #         targets (list[int]): List of users to enable

    #     Returns:
    #         list[User]: Enabled users
    #     """
    #     results = cls._request_list(
    #         http_method="PUT",
    #         adapter=adapter,
    #         endpoint="/user/{id}/reactivate",
    #         source=[{"id": target} for target in targets],
    #     )
    #     return [cls(**result) for result in results]

    # @classmethod
    # def resend_invite(
    #     cls: type[GWA], adapter: MetabaseApi, targets: list[int]
    # ) -> list[dict[str, bool]]:
    #     """Resent user invites

    #     Args:
    #         adapter (MetabaseApi): Connection to Metabase API
    #         targets (list[int]): List of users to resend invites for

    #     Returns:
    #         list[User]: Users with a resent invite
    #     """
    #     return cls._request_list(
    #         http_method="POST",
    #         adapter=adapter,
    #         endpoint="/user/{id}/send_invite",
    #         source=[{"id": target} for target in targets],
    #     )

    # @classmethod
    # def update_password(
    #     cls: type[GWA], adapter: MetabaseApi, payloads: list[dict[str, Any]]
    # ) -> list[GWA]:
    #     """Updates passwords for users

    #     Args:
    #         adapter (MetabaseApi): Connection to Metabase API
    #         payloads (list[dict]): List of users and passwords to update

    #     Returns:
    #         list[User]: List of users with reset passwords
    #     """
    #     results = cls._request_list(
    #         http_method="PUT",
    #         adapter=adapter,
    #         endpoint="/user/{id}/password",
    #         source=payloads,
    #     )
    #     return [cls(**result) for result in results]

    # @classmethod
    # def qbnewb(
    #     cls: type[GWA], adapter: MetabaseApi, targets: list[int]
    # ) -> list[dict[str, bool]]:
    #     """Indicate that a user has been informed about Query Builder.

    #     Args:
    #         adapter (MetabaseApi): Connection to Metabase API
    #         targets (list[int]): List of users to toggle

    #     Returns:
    #         list[Self]: Users with query builder toggle set
    #     """
    #     return cls._request_list(
    #         http_method="PUT",
    #         adapter=adapter,
    #         endpoint="/user/{id}/qbnewb",
    #         source=[{"id": target} for target in targets],
    #     )