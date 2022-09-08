"""Classes related to card endpoints
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any, ClassVar, Optional
from uuid import UUID

from pydantic import BaseModel, PrivateAttr
from pydantic.fields import Field

from metabase_tools.common import log_call, untested
from metabase_tools.exceptions import InvalidParameters
from metabase_tools.models.collection_model import CollectionItem
from metabase_tools.models.generic_model import Item
from metabase_tools.models.user_model import UserItem

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

logger = logging.getLogger(__name__)


class CardItem(Item):
    """Card object class with related methods"""

    _BASE_EP: ClassVar[str] = "/card/{id}"

    _adapter: Optional[MetabaseApi] = PrivateAttr(None)

    description: Optional[str]
    archived: bool
    collection_position: Optional[int]
    table_id: Optional[int]
    result_metadata: Optional[list[dict[str, Any]]]
    creator: UserItem
    database_id: Optional[int]
    enable_embedding: bool
    collection_id: Optional[int]
    query_type: Optional[str]
    creator_id: int
    updated_at: datetime
    made_public_by_id: Optional[int]
    embedding_params: Optional[dict[str, Any]]
    cache_ttl: Optional[str]
    dataset_query: dict[str, Any]
    display: str
    last_edit_info: Optional[dict[str, Any]] = Field(alias="last-edit-info")
    visualization_settings: dict[str, Any]
    collection: Optional[CollectionItem]
    dataset: Optional[int]
    created_at: datetime
    public_uuid: Optional[UUID]
    can_write: Optional[bool]
    dashboard_count: Optional[int]
    is_favorite: Optional[bool] = Field(alias="favorite")

    def set_adapter(self, adapter: MetabaseApi) -> None:
        """Sets the adapter on an object

        Args:
            adapter (MetabaseApi): Connection to MetabaseApi
        """
        super().set_adapter(adapter=adapter)

    @log_call
    def delete(self: CardItem) -> dict[int | str, dict[str, Any]]:
        """DEPRECATED; use archive instead

        Returns:
            dict[int | str, dict[str, Any]]: _description_
        """
        raise NotImplementedError

    @log_call
    def update(self: CardItem, payload: dict[str, Any]) -> CardItem:
        """Method for updating a card

        Args:
            payloads (dict): Details of update

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            CardItem: Object of the relevant type
        """
        return super().update(payload=payload)

    @log_call
    def archive(self: CardItem) -> CardItem:
        """Method for archiving a card

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            CardItem: Object of the relevant type
        """
        return super().archive()

    def unarchive(self: CardItem) -> CardItem:
        """Method for unarchiving a card

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            CardItem: Object of the relevant type
        """
        return super().unarchive()

    @log_call
    def related(self: CardItem) -> dict[str, Any]:
        """Objects related to target

        Returns:
            dict: Dict with related objects for target
        """
        new = {"card_id": self.id}
        if self._adapter:
            result = self._adapter.get(endpoint=f"/card/{self.id}/related")
            if isinstance(result, dict):
                return new | result
        raise InvalidParameters

    @log_call
    def favorite(self: CardItem) -> dict[str, Any]:
        """Mark card as favorite

        Returns:
            dict: Result of favoriting operation
        """
        if self._adapter:
            result = self._adapter.post(endpoint=f"/card/{self.id}/favorite")
            if isinstance(result, dict):
                return result
        raise InvalidParameters

    @log_call
    def unfavorite(self: CardItem) -> dict[str, Any]:
        """Unfavorite card

        Returns:
            dict: Result of unfavoriting operation
        """
        if self._adapter:
            result = self._adapter.delete(endpoint=f"/card/{self.id}/favorite")
            if isinstance(result, dict):
                return result
        raise InvalidParameters

    @untested
    def share(self: CardItem) -> dict[str, Any]:
        """Generate publicly-accessible link for card

        Returns:
            dict: UUID to be used in public link.
        """
        if self._adapter:
            result = self._adapter.post(endpoint=f"/card/{self.id}/public_link")
            if isinstance(result, dict):
                return result
        raise InvalidParameters

    @untested
    def unshare(self: CardItem) -> dict[str, Any]:
        """Remove publicly-accessible links for card

        Returns:
            dict: UUID to be used in public link.
        """
        if self._adapter:
            result = self._adapter.delete(endpoint=f"/card/{self.id}/public_link")
            if isinstance(result, dict):
                return result
        raise InvalidParameters

    @log_call
    def query(self: CardItem) -> CardQueryResult:
        """Execute a query stored in card(s)

        Returns:
            CardQueryResult: Results of query
        """
        if self._adapter:
            result = self._adapter.post(endpoint=f"/card/{self.id}/query")
            if isinstance(result, dict):
                return CardQueryResult(**result)
        raise InvalidParameters


class CardQueryResult(BaseModel):
    """Object for results of a card query"""

    data: dict[str, Any]
    database_id: int
    started_at: datetime
    json_query: dict[str, Any]
    average_execution_time: Optional[int]
    status: str
    context: str
    row_count: int
    running_time: int
