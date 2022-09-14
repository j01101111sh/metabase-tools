"""Classes related to user endpoints
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any, ClassVar, Optional

import packaging.version
from pydantic.fields import Field, PrivateAttr

from metabase_tools.common import log_call
from metabase_tools.exceptions import InvalidParameters
from metabase_tools.models.generic_model import Item

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

logger = logging.getLogger(__name__)


class UserItem(Item):
    """User object class with related methods"""

    _BASE_EP: ClassVar[str] = "/user/{id}"

    _adapter: Optional[MetabaseApi] = PrivateAttr(None)

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
    has_invited_second_user: Optional[bool]
    user_group_memberships: Optional[list[dict[str, int]]]
    first_login: Optional[datetime]
    has_question_and_dashboard: Optional[bool]
    is_installer: Optional[bool]
    sso_source: Optional[str]

    @log_call
    def disable(self) -> dict[int, Any]:
        """Disables user

        Returns:
            dict: Results
        """
        return super().delete()  # type: ignore

    @log_call
    def enable(self) -> UserItem:
        """Enable user

        Returns:
            UserItem: Enabled users
        """
        if self._adapter:
            result = self._adapter.put(endpoint=f"/user/{self.id}/reactivate")
            if isinstance(result, dict):
                obj = self.__class__(**result)
                obj.set_adapter(adapter=self._adapter)
                return obj
        raise InvalidParameters

    @log_call
    def resend_invite(self) -> dict[str, bool]:
        """Resent user invites

        Returns:
            UserItem: User with a resent invite
        """
        if self._adapter:
            result = self._adapter.post(endpoint=f"/user/{self.id}/send_invite")
            if isinstance(result, dict):
                return result
        raise InvalidParameters

    @log_call
    def update_password(self: UserItem, payload: dict[str, Any]) -> UserItem:
        """Updates passwords for users

        Args:
            payload (dict): New password

        Returns:
            UserItem: User with reset passwords
        """
        if self._adapter:
            result = self._adapter.put(
                endpoint=f"/user/{self.id}/password", json=payload
            )
            if isinstance(result, dict):
                obj = self.__class__(**result)
                obj.set_adapter(adapter=self._adapter)
                return obj
        raise InvalidParameters

    @log_call
    def qbnewb(self) -> dict[str, bool]:
        """Indicate that a user has been informed about Query Builder.

        Returns:
            UserItem: User with query builder toggle set
        """
        if self._server_version and self._server_version >= packaging.version.Version(
            "v0.42"
        ):
            raise NotImplementedError("This function was deprecated in Metabase v0.42")
        if self._adapter:
            result = self._adapter.put(endpoint=f"/user/{self.id}/qbnewb")
            if isinstance(result, dict):
                return result
        raise InvalidParameters
