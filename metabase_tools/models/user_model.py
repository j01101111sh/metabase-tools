"""Classes related to user endpoints
"""

from __future__ import annotations

from datetime import datetime
from logging import getLogger
from typing import TYPE_CHECKING, Any, ClassVar

from packaging.version import Version
from pydantic.fields import Field, PrivateAttr

from metabase_tools.models.generic_model import Item, MissingParam
from metabase_tools.utils.logging_utils import log_call

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

logger = getLogger(__name__)


class UserItem(Item):
    """User object class with related methods"""

    _BASE_EP: ClassVar[str] = "/user/{id}"

    _adapter: MetabaseApi | None = PrivateAttr(None)

    name: str = Field(alias="common_name")
    email: str
    first_name: str
    last_name: str
    date_joined: datetime
    last_login: datetime | None
    updated_at: datetime | None
    is_qbnewb: bool
    is_superuser: bool
    ldap_auth: bool | None
    google_auth: bool | None
    is_active: bool | None
    locale: str | None
    group_ids: list[int] | None
    login_attributes: list[dict[str, Any]] | None
    personal_collection_id: int | None
    has_invited_second_user: bool | None
    user_group_memberships: list[dict[str, int]] | None
    first_login: datetime | None
    has_question_and_dashboard: bool | None
    is_installer: bool | None
    sso_source: str | None

    @log_call
    def refresh(self: UserItem) -> UserItem:
        """Returns refreshed copy of the user

        Returns:
            UserItem: self
        """
        return super().refresh()

    @log_call
    def disable(self) -> None:
        """Disables user"""
        return super().delete()

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
            raise TypeError(f"Expected dict, received {type(result)}")
        raise AttributeError("Adapter not set on object")

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
            raise TypeError(f"Expected dict, received {type(result)}")
        raise AttributeError("Adapter not set on object")

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
            raise TypeError(f"Expected dict, received {type(result)}")
        raise AttributeError("Adapter not set on object")

    @log_call
    def qbnewb(self) -> dict[str, bool]:
        """Indicate that a user has been informed about Query Builder.

        Returns:
            UserItem: User with query builder toggle set
        """
        if self._server_version and self._server_version >= Version("v0.42"):
            raise NotImplementedError("This function was deprecated in Metabase v0.42")
        if self._adapter:
            result = self._adapter.put(endpoint=f"/user/{self.id}/qbnewb")
            if isinstance(result, dict):
                return result
            raise TypeError(f"Expected dict, received {type(result)}")
        raise AttributeError("Adapter not set on object")

    def _make_update(self: UserItem, **kwargs: Any) -> UserItem:
        """Makes update request

        Args:
            self (UserItem)

        Returns:
            UserItem: self
        """
        return super()._make_update(**kwargs)

    @log_call
    def update(
        self: UserItem,
        email: str | MissingParam | None = MissingParam(),
        first_name: str | MissingParam | None = MissingParam(),
        is_group_manager: bool | MissingParam | None = MissingParam(),
        locale: str | MissingParam | None = MissingParam(),
        user_group_memberships: list[int] | MissingParam | None = MissingParam(),
        is_superuser: bool | MissingParam | None = MissingParam(),
        login_attributes: str | MissingParam | None = MissingParam(),
        last_name: str | MissingParam | None = MissingParam(),
        **kwargs: Any,
    ) -> UserItem:
        """Updates a user using the provided parameters

        Args:
            self (UserItem)
            email (str, optional)
            first_name (str, optional)
            is_group_manager (bool, optional)
            locale (str, optional)
            user_group_memberships (list[int], optional)
            is_superuser (bool, optional)
            login_attributes (str, optional)
            last_name (str, optional)

        Returns:
            UserItem
        """
        return self._make_update(
            email=email,
            first_name=first_name,
            is_group_manager=is_group_manager,
            locale=locale,
            user_group_memberships=user_group_memberships,
            is_superuser=is_superuser,
            login_attributes=login_attributes,
            last_name=last_name,
            **kwargs,
        )
