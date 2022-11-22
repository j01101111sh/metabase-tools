"""Classes related to dashboard endpoints
"""
from __future__ import annotations

from datetime import datetime
from logging import getLogger
from typing import TYPE_CHECKING, Any, ClassVar, Optional

from pydantic import PrivateAttr

from metabase_tools.models.generic_model import Item, MissingParam
from metabase_tools.models.user_model import UserItem
from metabase_tools.utils.logging_utils import log_call

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

logger = getLogger(__name__)


class DashboardItem(Item):
    """Dashboard object class with related methods"""

    _BASE_EP: ClassVar[str] = "/dashboard/{id}"

    _adapter: Optional[MetabaseApi] = PrivateAttr(None)

    description: Optional[str]
    archived: bool
    collection_position: Optional[int]
    creator: Optional[UserItem]
    enable_embedding: bool
    collection_id: Optional[int]
    show_in_getting_started: bool
    name: str
    caveats: Optional[list[str]]
    creator_id: int
    updated_at: datetime
    made_public_by_id: Optional[int]
    embedding_params: Optional[dict[str, Any]]
    id: int
    position: Optional[int]
    parameters: list[dict[str, Any]]
    favorite: Optional[bool]
    created_at: datetime
    public_uuid: Optional[str]
    points_of_interest: Optional[str]
    can_write: Optional[bool]
    ordered_cards: Optional[list[int]]
    param_fields: Optional[dict[str, Any]]
    param_values: Optional[dict[str, Any]]

    @log_call
    def refresh(self: DashboardItem) -> DashboardItem:
        """Returns refreshed copy of the dashboard

        Returns:
            DashboardItem: self
        """
        return super().refresh()

    @log_call
    def delete(self: DashboardItem) -> None:
        """Deletes the dashboard"""
        return super().delete()

    def _make_update(self: DashboardItem, **kwargs: Any) -> DashboardItem:
        """Makes update request

        Args:
            self (DashboardItem)

        Returns:
            DashboardItem: self
        """
        return super()._make_update(**kwargs)

    @log_call
    def update(
        self: DashboardItem,
        engine: Optional[str | MissingParam] = MissingParam(),
        schedules: Optional[dict[str, Any] | MissingParam] = MissingParam(),
        refingerprint: Optional[bool | MissingParam] = MissingParam(),
        points_of_interest: Optional[str | MissingParam] = MissingParam(),
        description: Optional[str | MissingParam] = MissingParam(),
        name: Optional[str | MissingParam] = MissingParam(),
        caveats: Optional[str | MissingParam] = MissingParam(),
        cache_ttl: Optional[int | MissingParam] = MissingParam(),
        details: Optional[dict[str, Any] | MissingParam] = MissingParam(),
        **kwargs: Any,
    ) -> DashboardItem:
        """Updates a dashboard using the provided parameters

        Args:
            self (DashboardItem)
            engine (str, optional)
            schedules (dict[str, Any], optional)
            refingerprint (bool, optional)
            points_of_interest (str, optional)
            description (str, optional)
            name (str, optional)
            caveats (str, optional)
            cache_ttl (int, optional)
            details (dict[str, Any], optional)

        Returns:
            DashboardItem
        """
        return self._make_update(
            engine=engine,
            schedules=schedules,
            refingerprint=refingerprint,
            points_of_interest=points_of_interest,
            description=description,
            name=name,
            caveats=caveats,
            cache_ttl=cache_ttl,
            details=details,
            **kwargs,
        )
