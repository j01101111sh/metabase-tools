"""Classes related to dashboard endpoints
"""

from __future__ import annotations

from datetime import datetime
from logging import getLogger
from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import Field, PrivateAttr

from metabase_tools.models.generic_model import Item, MissingParam
from metabase_tools.models.user_model import UserItem
from metabase_tools.utils.logging_utils import log_call

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

logger = getLogger(__name__)


class DashboardItem(Item):
    """Dashboard object class with related methods"""

    _BASE_EP: ClassVar[str] = "/dashboard/{id}"

    _adapter: MetabaseApi | None = PrivateAttr(None)

    description: str | None
    archived: bool
    collection_position: int | None
    creator: UserItem | None
    enable_embedding: bool
    collection_id: int | None
    show_in_getting_started: bool
    name: str
    caveats: str | None
    creator_id: int
    updated_at: datetime
    made_public_by_id: int | None
    embedding_params: dict[str, Any] | None
    id: int
    position: int | None
    parameters: list[dict[str, Any]]
    favorite: bool | None
    created_at: datetime
    public_uuid: str | None
    points_of_interest: str | None
    can_write: bool | None
    ordered_cards: list[dict[str, Any]] | None
    param_fields: dict[str, Any] | None
    param_values: dict[str, Any] | None
    cache_ttl: int | None
    entity_id: str | None
    last_edit_info: dict[str, Any] | None = Field(alias="last-edit-info")
    collection_authority_level: int | None
    is_app_page: bool | None

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
        parameters: list[dict[str, Any]] | MissingParam | None = MissingParam(),
        points_of_interest: str | MissingParam | None = MissingParam(),
        description: str | MissingParam | None = MissingParam(),
        archived: bool | MissingParam | None = MissingParam(),
        collection_position: int | MissingParam | None = MissingParam(),
        show_in_getting_started: bool | MissingParam | None = MissingParam(),
        enabled_embedding: bool | MissingParam | None = MissingParam(),
        collection_id: int | MissingParam | None = MissingParam(),
        name: str | MissingParam | None = MissingParam(),
        caveats: str | MissingParam | None = MissingParam(),
        embedding_params: dict[str, Any] | MissingParam | None = MissingParam(),
        position: int | MissingParam | None = MissingParam(),
        **kwargs: Any,
    ) -> DashboardItem:
        """Updates an existing dashboard item

        Args:
            self (DashboardItem)
            parameters (list[dict[str, Any]], optional)
            points_of_interest (str, optional)
            description (str, optional)
            archived (bool, optional)
            collection_position (int, optional)
            show_in_getting_started (bool, optional)
            enabled_embedding (bool, optional)
            collection_id (int, optional)
            name (str, optional)
            caveats (str, optional)
            embedding_params (dict[str, Any], optional)
            position (int, optional)

        Returns:
            DashboardItem: _description_
        """
        return self._make_update(
            parameters=parameters,
            points_of_interest=points_of_interest,
            description=description,
            archived=archived,
            collection_position=collection_position,
            show_in_getting_started=show_in_getting_started,
            enabled_embedding=enabled_embedding,
            collection_id=collection_id,
            name=name,
            caveats=caveats,
            embedding_params=embedding_params,
            position=position,
            **kwargs,
        )
