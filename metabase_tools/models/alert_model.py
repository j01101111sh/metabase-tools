"""Classes related to alert endpoints
"""

from __future__ import annotations

from datetime import datetime
from logging import getLogger
from typing import TYPE_CHECKING, Any, ClassVar

from packaging.version import Version
from pydantic import PrivateAttr
from pydantic.fields import Field

from metabase_tools.exceptions import MetabaseApiException
from metabase_tools.models.generic_model import Item, MissingParam
from metabase_tools.models.user_model import UserItem
from metabase_tools.utils.logging_utils import log_call

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

logger = getLogger(__name__)


class AlertItem(Item):
    """Alert object class with related methods"""

    _BASE_EP: ClassVar[str] = "/alert/{id}"

    _adapter: MetabaseApi | None = PrivateAttr(None)
    _server_version: Version | None = PrivateAttr(None)

    archived: bool
    collection_position: int | None
    creator: UserItem
    can_write: bool | None
    channels: list[dict[str, Any]]
    alert_condition: str
    collection_id: int | None
    creator_id: int
    card: dict[str, Any]
    updated_at: datetime
    alert_first_only: bool
    lower_name: str | None = Field(alias="lower-name")
    entity_id: str | None
    skip_if_empty: bool
    parameters: list[dict[str, Any]]
    dashboard_id: int | None
    created_at: datetime
    alert_above_goal: bool | None

    @log_call
    def set_adapter(self, adapter: MetabaseApi) -> None:
        """Sets the adapter on an object

        Args:
            adapter (MetabaseApi): Connection to MetabaseApi
        """
        super().set_adapter(adapter=adapter)

    @log_call
    def refresh(self: AlertItem) -> AlertItem:
        """Returns refreshed copy of the alert

        Returns:
            AlertItem: self
        """
        if self._adapter and self._adapter.server_version >= Version("v0.41"):
            return super().refresh()
        if self._adapter and isinstance(self.id, int):
            return self._adapter.alerts.get(targets=[self.id])[0]
        raise MetabaseApiException

    @log_call
    def delete(self: AlertItem) -> None:
        """DEPRECATED; use archive instead"""
        raise NotImplementedError

    def _make_update(self: AlertItem, **kwargs: Any) -> AlertItem:
        """Makes update request

        Args:
            self (AlertItem)

        Returns:
            AlertItem: self
        """
        return super()._make_update(**kwargs)

    @log_call
    def update(
        self: AlertItem,
        alert_condition: str | MissingParam | None = MissingParam(),
        alert_first_only: bool | MissingParam | None = MissingParam(),
        alert_above_goal: bool | MissingParam | None = MissingParam(),
        card: dict[str, Any] | MissingParam | None = MissingParam(),
        channels: list[dict[str, Any]] | MissingParam | None = MissingParam(),
        archived: bool | MissingParam | None = MissingParam(),
        **kwargs: Any,
    ) -> AlertItem:
        """Updates a card using the provided parameters

        Args:
            self (AlertItem): _description_
            alert_condition (str, optional)
            alert_first_only (bool, optional)
            alert_above_goal (bool, optional)
            card (dict[str, Any], optional)
            channels (list[dict[str, Any]], optional)
            archived (bool, optional)

        Returns:
            AlertItem: _description_
        """
        return self._make_update(
            alert_condition=alert_condition,
            alert_first_only=alert_first_only,
            alert_above_goal=alert_above_goal,
            card=card,
            channels=channels,
            archived=archived,
            **kwargs,
        )

    @log_call
    def archive(self: AlertItem) -> AlertItem:
        """Method for archiving an alert

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            AlertItem: Object of the relevant type
        """
        return super().archive()

    @log_call
    def unarchive(self: AlertItem) -> AlertItem:
        """Method for unarchiving an alert

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            AlertItem: Object of the relevant type
        """
        return super().unarchive()
